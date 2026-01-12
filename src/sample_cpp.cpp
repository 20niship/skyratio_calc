#include "scene_raycaster.hpp"
#include "sky_ratio_checker.hpp"
#include <iomanip>
#include <iostream>

int main() {
  std::cout << "=== 天空率計算サンプル ===" << std::endl;

  // シーンの作成
  SceneRaycaster scene;

  // 建物を追加(ボックス)
  scene.add_box({5.0, 0.0, 0.0}, {2.0, 2.0, 10.0}, {0.0, 0.0, 0.0});
  scene.add_box({-5.0, 0.0, 0.0}, {2.0, 2.0, 8.0}, {0.0, 0.0, 0.0});

  // 球体を追加
  scene.add_sphere({0.0, 8.0, 5.0}, 2.0);

  // BVHをビルド
  scene.build();
  std::cout << "シーンを構築しました" << std::endl;

  // 天空率チェッカーの作成
  SkyRatioChecker checker;
  checker.set_scene(scene);
  checker.ray_resolution = 5.0f; // 5度刻み

  // 測定点を追加
  checker.checkpoints.push_back({0.0, 0.0, 1.5});  // 原点付近
  checker.checkpoints.push_back({3.0, 0.0, 1.5});  // 建物に近い位置
  checker.checkpoints.push_back({10.0, 0.0, 1.5}); // 離れた位置

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  // 天空率を計算
  std::cout << "\n天空率を計算中..." << std::endl;
  auto sky_ratios = checker.check();

  // 結果を表示
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }

  return 0;
}
