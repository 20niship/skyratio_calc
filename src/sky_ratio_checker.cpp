#include "sky_ratio_checker.hpp"
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// 天頂角の範囲設定（レイキャストの負荷軽減のため）
static const double THETA_MIN_DEG = 20.0;
static const double THETA_MAX_DEG = 89.0;

std::vector<std::tuple<Vec3, Vec3>> SkyRatioChecker::generate_rays_from_checkpoint(const Vec3& checkpoint) {
  std::vector<std::tuple<Vec3, Vec3>> rays;

  // ray_resolutionの妥当性チェック
  if(ray_resolution <= 0.0f || ray_resolution > 180.0f) {
    ray_resolution = 1.0f; // デフォルト値に設定
  }

  // 天空率は天頂方向を中心とした半球について計算
  double resolution_rad = ray_resolution * M_PI / 180.0;

  // 天頂角(theta): 20度から89度までに変更（負荷軽減のため）
  int theta_steps = static_cast<int>((THETA_MAX_DEG - THETA_MIN_DEG) / ray_resolution);
  
  // 方位角(phi): 0度から360度まで
  int phi_steps = static_cast<int>(360.0 / ray_resolution);

  // phi_stepsが0になるのを防ぐ
  if(phi_steps < 1) phi_steps = 1;

  for(int t = 0; t <= theta_steps; t++) {
    double theta = (THETA_MIN_DEG + t * ray_resolution) * M_PI / 180.0;
    double sin_theta = std::sin(theta);
    double cos_theta = std::cos(theta);

    for(int p = 0; p < phi_steps; p++) {
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

    // レイキャスト実行
    auto hit_results = raycaster->raycast(origins, directions);

    // 三斜求積法による天空率の計算
    double resolution_rad = ray_resolution * M_PI / 180.0;
    
    // 方位角の分割数
    int phi_steps = static_cast<int>(360.0 / ray_resolution);
    if(phi_steps < 1) phi_steps = 1;
    
    int theta_steps = static_cast<int>((THETA_MAX_DEG - THETA_MIN_DEG) / ray_resolution);

    // 各方位角(phi)における、空が見える最小天頂角を格納する配列
    std::vector<double> visible_theta(phi_steps);
    
    // 初期値: THETA_MIN_DEGより低い角度は検査しないため、
    // 0度（天頂）から検査開始角度までは空が見えると仮定
    double theta_min_rad = THETA_MIN_DEG * M_PI / 180.0;
    for(int p = 0; p < phi_steps; p++) {
      visible_theta[p] = 0.0;
    }

    // レイキャスト結果から、各方位角で空が見える最小天頂角を求める
    // 方位角ごとにループを回し、各方向で最初に空が見える角度を探す
    for(int p = 0; p < phi_steps; p++) {
      // この方位角での最大遮蔽角度（空が見え始める角度）
      double max_blocked_theta = 0.0;
      
      for(int t = 0; t <= theta_steps; t++) {
        double theta = (THETA_MIN_DEG + t * ray_resolution) * M_PI / 180.0;
        int ray_index = t * phi_steps + p;
        
        if(ray_index < hit_results.size() && hit_results[ray_index].hit) {
          // 建物にヒット → この角度では空が見えない
          double blocked_theta = theta;
          
          // 安全側評価の適用
          if(use_safe_side) {
            // 内接近似：建物を大きく見積もる（空を小さく見積もる）
            blocked_theta += resolution_rad;
          } else {
            // 外接近似：建物を小さく見積もる（空を大きく見積もる）
            blocked_theta -= resolution_rad;
          }
          
          // 範囲制限: 90度を超えないようにする
          if(blocked_theta > M_PI / 2.0) blocked_theta = M_PI / 2.0;
          
          // この方位角で最も遮られた角度を更新
          if(blocked_theta > max_blocked_theta) {
            max_blocked_theta = blocked_theta;
          }
        }
      }
      
      visible_theta[p] = max_blocked_theta;
    }

    // 三斜求積法による面積計算
    // 各方位角間で扇形セグメントの面積を計算し合計する
    double sky_area = 0.0;
    double d_phi = 2.0 * M_PI / phi_steps; // 方位角の刻み

    for(int p = 0; p < phi_steps; p++) {
      int p_next = (p + 1) % phi_steps;
      
      // 2つの隣接する方位角での空が見える開始角度（遮蔽終了角度）
      double theta1 = visible_theta[p];
      double theta2 = visible_theta[p_next];
      
      // 正射影上の面積：各方位角での天頂角からの寄与
      // 天頂角θから90°までの正射影面積の重みは cos²(θ)
      // 2つの方位角での平均を取り、扇形の角度dφを掛ける
      double area_weight1 = std::cos(theta1) * std::cos(theta1);
      double area_weight2 = std::cos(theta2) * std::cos(theta2);
      double avg_weight = (area_weight1 + area_weight2) / 2.0;
      
      // このセグメントの面積
      double segment_area = 0.5 * avg_weight * d_phi;
      
      sky_area += segment_area;
    }

    // 全天の投影面積はπ（半径1の円）
    double total_area = M_PI;
    float sky_ratio = static_cast<float>(sky_area / total_area);
    
    // 範囲制限
    if(sky_ratio < 0.0f) sky_ratio = 0.0f;
    if(sky_ratio > 1.0f) sky_ratio = 1.0f;
    
    results.push_back(sky_ratio);
  }

  return results;
}
