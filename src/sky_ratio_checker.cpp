#include "sky_ratio_checker.hpp"
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

std::vector<std::tuple<Vec3, Vec3>> SkyRatioChecker::generate_rays_from_checkpoint(const Vec3 &checkpoint) {
    std::vector<std::tuple<Vec3, Vec3>> rays;
    
    // 天空率は天頂方向を中心とした半球について計算
    double resolution_rad = ray_resolution * M_PI / 180.0;
    
    // 天頂角(theta): 0度(真上)から90度(水平)まで
    int theta_steps = static_cast<int>(90.0 / ray_resolution);
    // 方位角(phi): 0度から360度まで
    int phi_steps = static_cast<int>(360.0 / ray_resolution);
    
    for (int t = 0; t <= theta_steps; t++) {
        double theta = t * resolution_rad;
        double sin_theta = std::sin(theta);
        double cos_theta = std::cos(theta);
        
        // 天頂(theta=0)の場合は1本のレイのみ
        int current_phi_steps = (t == 0) ? 1 : phi_steps;
        
        for (int p = 0; p < current_phi_steps; p++) {
            double phi = p * 2.0 * M_PI / phi_steps;
            
            // 球面座標から直交座標への変換
            Vec3 direction = {
                sin_theta * std::cos(phi),
                sin_theta * std::sin(phi),
                cos_theta  // Z軸を上方向とする
            };
            
            rays.push_back(std::make_tuple(checkpoint, direction));
        }
    }
    
    return rays;
}

void SkyRatioChecker::set_scene(const SceneRaycaster &scene) {
    raycaster = scene;
}

std::vector<float> SkyRatioChecker::check() {
    std::vector<float> results;
    results.reserve(checkpoints.size());
    
    for (const auto &checkpoint : checkpoints) {
        auto rays = generate_rays_from_checkpoint(checkpoint);
        
        // レイの原点と方向を分離
        std::vector<Vec3> origins, directions;
        origins.reserve(rays.size());
        directions.reserve(rays.size());
        
        for (const auto &ray : rays) {
            origins.push_back(std::get<0>(ray));
            directions.push_back(std::get<1>(ray));
        }
        
        // レイキャスト実行
        auto hit_results = raycaster.raycast(origins, directions);
        
        // ヒットしなかったレイの数をカウント(=天空が見えている)
        int sky_visible_count = 0;
        for (const auto &result : hit_results) {
            if (!result.hit) {
                sky_visible_count++;
            }
        }
        
        // 天空率を計算
        float sky_ratio = static_cast<float>(sky_visible_count) / static_cast<float>(rays.size());
        results.push_back(sky_ratio);
    }
    
    return results;
}
