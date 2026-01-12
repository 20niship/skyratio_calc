#include "sky_ratio_checker.hpp"
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

std::vector<std::tuple<Vec3, Vec3>> SkyRatioChecker::generate_rays_from_checkpoint(const Vec3& checkpoint) {
  std::vector<std::tuple<Vec3, Vec3>> rays;

  // ray_resolutionの妥当性チェック
  if(ray_resolution <= 0.0f || ray_resolution > 180.0f) {
    ray_resolution = 1.0f; // デフォルト値に設定
  }

  // 天空率は天頂方向を中心とした半球について計算
  double resolution_rad = ray_resolution * M_PI / 180.0;

  // 天頂角(theta): 0度(真上)から90度(水平)まで
  int theta_steps = static_cast<int>(90.0 / ray_resolution);
  // 方位角(phi): 0度から360度まで
  int phi_steps = static_cast<int>(360.0 / ray_resolution);

  // phi_stepsが0になるのを防ぐ
  if(phi_steps < 1) phi_steps = 1;

  for(int t = 0; t <= theta_steps; t++) {
    double theta     = t * resolution_rad;
    double sin_theta = std::sin(theta);
    double cos_theta = std::cos(theta);

    // 天頂(theta=0)の場合は1本のレイのみ
    int current_phi_steps = (t == 0) ? 1 : phi_steps;

    for(int p = 0; p < current_phi_steps; p++) {
      double phi = p * 2.0 * M_PI / phi_steps;

      // 球面座標から直交座標への変換
      Vec3 direction = {
        sin_theta * std::cos(phi), sin_theta * std::sin(phi),
        cos_theta // Z軸を上方向とする
      };

      rays.push_back(std::make_tuple(checkpoint, direction));
    }
  }

  return rays;
}

void SkyRatioChecker::set_scene(const SceneRaycaster& scene) { raycaster = &scene; }

std::vector<float> SkyRatioChecker::check() {
  std::vector<float> results;
  results.reserve(checkpoints.size());

  if(!raycaster) {
    return results;
  }

  for(const auto& checkpoint : checkpoints) {
    auto rays = generate_rays_from_checkpoint(checkpoint);

    // レイの原点と方向を分離
    std::vector<Vec3> origins, directions;
    origins.reserve(rays.size());
    directions.reserve(rays.size());

    for(const auto& ray : rays) {
      origins.push_back(std::get<0>(ray));
      directions.push_back(std::get<1>(ray));
    }

    // レイキャスト実行（一度だけ）
    auto hit_results = raycaster->raycast(origins, directions);

    // 積分計算による天空率の計算
    double resolution_rad = ray_resolution * M_PI / 180.0;

    int theta_steps = static_cast<int>(90.0 / ray_resolution);
    int phi_steps   = static_cast<int>(360.0 / ray_resolution);
    if(phi_steps < 1) phi_steps = 1;

    // 空が見える部分の投影面積を計算
    double sky_area = 0.0;
    int ray_index   = 0;

    for(int t = 0; t <= theta_steps; t++) {
      // レイの角度に対応するセルの範囲を計算
      double theta_start = t * resolution_rad;
      double theta_end   = (t + 1) * resolution_rad;
      if(theta_end > M_PI / 2.0) theta_end = M_PI / 2.0;

      int current_phi_steps = (t == 0) ? 1 : phi_steps;

      // このthetaセルの投影面積の重み（phi方向の積分なし）
      double theta_area = (std::sin(theta_end) * std::sin(theta_end) - std::sin(theta_start) * std::sin(theta_start)) / 2.0;

      for(int p = 0; p < current_phi_steps; p++) {
        if(ray_index < hit_results.size() && !hit_results[ray_index].hit) {
          if(t == 0) {
            // 天頂の場合は全周（2π）を代表
            sky_area += theta_area * 2.0 * M_PI;
          } else {
            // 通常のセルは dPhi の範囲を代表
            double dPhi = 2.0 * M_PI / phi_steps;
            sky_area += theta_area * dPhi;
          }
        }
        ray_index++;
      }
    }

    // 全天の投影面積はπ（半径1の円）
    double total_area = M_PI;
    float sky_ratio   = static_cast<float>(sky_area / total_area);
    results.push_back(sky_ratio);
  }

  return results;
}
