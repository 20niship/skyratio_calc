#pragma once

#include <array>
#include <vector>
#include <cmath>

using Vec3 = std::array<double, 3>;

struct HitResult {
    bool hit = false;
    Vec3 position = {0.0, 0.0, 0.0};
    double distance = 0.0;
};

struct Box {
    Vec3 center;
    Vec3 size;
    Vec3 euler;
};

struct Sphere {
    Vec3 center;
    double radius;
};

class SceneRaycaster {
private:
    bool build_dirty = true;
    std::vector<Box> boxes;
    std::vector<Sphere> spheres;
    std::vector<float> vertices;
    std::vector<unsigned int> indices;

public:
    void clear();
    void add_box(const Vec3 &pos, const Vec3 &size, const Vec3 &euler);
    void add_sphere(const Vec3 &center, double radius);
    void add_mesh(const std::vector<Vec3> &mesh_vertices);
    void build();
    std::vector<HitResult> raycast(const std::vector<Vec3> &origins, const std::vector<Vec3> &directions);
};
