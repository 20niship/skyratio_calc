#include "scene_raycaster.hpp"
#include <cmath>
#include <limits>
#include <algorithm>

#define TINYBVH_IMPLEMENTATION
#include "ext/tinybvh/tiny_bvh.h"

namespace {
    // 回転行列を生成(オイラー角から)
    std::array<std::array<double, 3>, 3> euler_to_rotation_matrix(const Vec3 &euler) {
        double cx = std::cos(euler[0]), sx = std::sin(euler[0]);
        double cy = std::cos(euler[1]), sy = std::sin(euler[1]);
        double cz = std::cos(euler[2]), sz = std::sin(euler[2]);
        
        return {{
            {cy * cz, -cy * sz, sy},
            {sx * sy * cz + cx * sz, -sx * sy * sz + cx * cz, -sx * cy},
            {-cx * sy * cz + sx * sz, cx * sy * sz + sx * cz, cx * cy}
        }};
    }

    // ベクトルと行列の積
    Vec3 matrix_vector_multiply(const std::array<std::array<double, 3>, 3> &mat, const Vec3 &vec) {
        return {
            mat[0][0] * vec[0] + mat[0][1] * vec[1] + mat[0][2] * vec[2],
            mat[1][0] * vec[0] + mat[1][1] * vec[1] + mat[1][2] * vec[2],
            mat[2][0] * vec[0] + mat[2][1] * vec[1] + mat[2][2] * vec[2]
        };
    }

    // レイと球の交差判定
    bool intersect_ray_sphere(const Vec3 &origin, const Vec3 &direction, 
                             const Sphere &sphere, double &t) {
        Vec3 oc = {origin[0] - sphere.center[0], 
                   origin[1] - sphere.center[1], 
                   origin[2] - sphere.center[2]};
        
        double a = direction[0] * direction[0] + direction[1] * direction[1] + direction[2] * direction[2];
        double b = 2.0 * (oc[0] * direction[0] + oc[1] * direction[1] + oc[2] * direction[2]);
        double c = oc[0] * oc[0] + oc[1] * oc[1] + oc[2] * oc[2] - sphere.radius * sphere.radius;
        
        double discriminant = b * b - 4 * a * c;
        if (discriminant < 0) return false;
        
        double sqrt_disc = std::sqrt(discriminant);
        double t0 = (-b - sqrt_disc) / (2.0 * a);
        double t1 = (-b + sqrt_disc) / (2.0 * a);
        
        if (t0 > 0.0001) {
            t = t0;
            return true;
        }
        if (t1 > 0.0001) {
            t = t1;
            return true;
        }
        return false;
    }

    // レイとAABBの交差判定
    bool intersect_ray_aabb(const Vec3 &origin, const Vec3 &direction,
                           const Vec3 &min_bound, const Vec3 &max_bound, double &t) {
        double tmin = 0.0, tmax = std::numeric_limits<double>::max();
        
        for (int i = 0; i < 3; i++) {
            if (std::abs(direction[i]) < 1e-8) {
                if (origin[i] < min_bound[i] || origin[i] > max_bound[i])
                    return false;
            } else {
                double t1 = (min_bound[i] - origin[i]) / direction[i];
                double t2 = (max_bound[i] - origin[i]) / direction[i];
                if (t1 > t2) std::swap(t1, t2);
                tmin = std::max(tmin, t1);
                tmax = std::min(tmax, t2);
                if (tmin > tmax) return false;
            }
        }
        
        if (tmin > 0.0001) {
            t = tmin;
            return true;
        }
        return false;
    }
}

void SceneRaycaster::clear() {
    boxes.clear();
    spheres.clear();
    vertices.clear();
    indices.clear();
    build_dirty = true;
}

void SceneRaycaster::add_box(const Vec3 &pos, const Vec3 &size, const Vec3 &euler) {
    boxes.push_back({pos, size, euler});
    build_dirty = true;
}

void SceneRaycaster::add_sphere(const Vec3 &center, double radius) {
    spheres.push_back({center, radius});
    build_dirty = true;
}

void SceneRaycaster::add_mesh(const std::vector<Vec3> &mesh_vertices) {
    size_t base_idx = vertices.size() / 3;
    
    for (const auto &v : mesh_vertices) {
        vertices.push_back(static_cast<float>(v[0]));
        vertices.push_back(static_cast<float>(v[1]));
        vertices.push_back(static_cast<float>(v[2]));
    }
    
    // 三角形として登録
    for (size_t i = 0; i < mesh_vertices.size() / 3; i++) {
        indices.push_back(static_cast<unsigned int>(base_idx + i * 3));
        indices.push_back(static_cast<unsigned int>(base_idx + i * 3 + 1));
        indices.push_back(static_cast<unsigned int>(base_idx + i * 3 + 2));
    }
    
    build_dirty = true;
}

void SceneRaycaster::build() {
    // ボックスをメッシュに変換
    for (const auto &box : boxes) {
        auto rot_mat = euler_to_rotation_matrix(box.euler);
        Vec3 half_size = {box.size[0] / 2, box.size[1] / 2, box.size[2] / 2};
        
        // ボックスの8頂点
        std::vector<Vec3> corners(8);
        for (int i = 0; i < 8; i++) {
            Vec3 local = {
                (i & 1) ? half_size[0] : -half_size[0],
                (i & 2) ? half_size[1] : -half_size[1],
                (i & 4) ? half_size[2] : -half_size[2]
            };
            Vec3 rotated = matrix_vector_multiply(rot_mat, local);
            corners[i] = {
                rotated[0] + box.center[0],
                rotated[1] + box.center[1],
                rotated[2] + box.center[2]
            };
        }
        
        // ボックスの12三角形(6面 × 2三角形)
        std::vector<std::array<int, 3>> faces = {
            {0,1,2}, {2,1,3}, // 前
            {4,6,5}, {5,6,7}, // 後
            {0,2,4}, {4,2,6}, // 左
            {1,5,3}, {3,5,7}, // 右
            {0,4,1}, {1,4,5}, // 下
            {2,3,6}, {6,3,7}  // 上
        };
        
        size_t base_idx = vertices.size() / 3;
        for (const auto &corner : corners) {
            vertices.push_back(static_cast<float>(corner[0]));
            vertices.push_back(static_cast<float>(corner[1]));
            vertices.push_back(static_cast<float>(corner[2]));
        }
        
        for (const auto &face : faces) {
            indices.push_back(static_cast<unsigned int>(base_idx + face[0]));
            indices.push_back(static_cast<unsigned int>(base_idx + face[1]));
            indices.push_back(static_cast<unsigned int>(base_idx + face[2]));
        }
    }
    
    build_dirty = false;
}

std::vector<HitResult> SceneRaycaster::raycast(const std::vector<Vec3> &origins, 
                                                const std::vector<Vec3> &directions) {
    if (build_dirty) build();
    
    std::vector<HitResult> results(origins.size());
    
    // BVHを使用する場合(メッシュがある場合)
    if (!vertices.empty() && !indices.empty()) {
        tinybvh::BVH bvh;
        bvh.Build(reinterpret_cast<tinybvh::bvhvec4*>(vertices.data()), vertices.size() / 3);
        
        for (size_t i = 0; i < origins.size(); i++) {
            tinybvh::Ray ray(
                tinybvh::bvhvec3(static_cast<float>(origins[i][0]), 
                                 static_cast<float>(origins[i][1]), 
                                 static_cast<float>(origins[i][2])),
                tinybvh::bvhvec3(static_cast<float>(directions[i][0]), 
                                 static_cast<float>(directions[i][1]), 
                                 static_cast<float>(directions[i][2]))
            );
            
            bvh.Intersect(ray);
            
            if (ray.hit.t < 1e30f) {
                results[i].hit = true;
                results[i].distance = ray.hit.t;
                results[i].position[0] = origins[i][0] + directions[i][0] * ray.hit.t;
                results[i].position[1] = origins[i][1] + directions[i][1] * ray.hit.t;
                results[i].position[2] = origins[i][2] + directions[i][2] * ray.hit.t;
            }
        }
    }
    
    // 球との交差判定
    for (size_t i = 0; i < origins.size(); i++) {
        double closest_t = results[i].hit ? results[i].distance : std::numeric_limits<double>::max();
        bool hit_sphere = false;
        
        for (const auto &sphere : spheres) {
            double t;
            if (intersect_ray_sphere(origins[i], directions[i], sphere, t)) {
                if (t < closest_t) {
                    closest_t = t;
                    hit_sphere = true;
                    results[i].hit = true;
                    results[i].distance = t;
                    results[i].position[0] = origins[i][0] + directions[i][0] * t;
                    results[i].position[1] = origins[i][1] + directions[i][1] * t;
                    results[i].position[2] = origins[i][2] + directions[i][2] * t;
                }
            }
        }
    }
    
    return results;
}
