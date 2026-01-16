#include "scene_raycaster.hpp"
#include "sky_ratio_checker.hpp"
#include <iomanip>
#include <iostream>

void test_no_obstacles() {
  SceneRaycaster scene;
  SkyRatioChecker checker;
  checker.ray_resolution = 10.0f;                 // 10度刻み
  checker.checkpoints.push_back({0.0, 0.0, 1.5}); // 原点付近

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  auto sky_ratios = checker.check(&scene);
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
}

void test_large_wall_blocks_half_hemisphere() {
  SceneRaycaster scene;
  scene.add_box({0.0, 2.0, 50.0}, {100.0, 1.0, 100.0}, {0.0, 0.0, 0.0});
  SkyRatioChecker checker;
  checker.checkpoints.push_back({0.0, 0.0, 1.5}); // 原点付近

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  auto sky_ratios = checker.check(&scene);
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
}

void test_many_small_objects_far_away() {
  SceneRaycaster scene;
  // 小さなボックス（1m x 1m x 1m）を40個、測定点から離して配置
  int num_boxes = 40;
  double radius = 50.0; // 測定点から50m離れた円周上に配置

  for(int i = 0; i < num_boxes; i++) {
    double angle = 2.0 * M_PI * i / num_boxes;
    double x     = radius * std::cos(angle);
    double y     = radius * std::sin(angle);
    double z     = 5.0; // 地面より少し上
    scene.add_box({x, y, z}, {1.0, 1.0, 1.0}, {0.0, 0.0, 0.0});
  }

  SkyRatioChecker checker;
  checker.ray_resolution = 5.0f;                  // 5度刻み
  checker.checkpoints.push_back({0.0, 0.0, 1.5}); // 原点付近

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  auto sky_ratios = checker.check(&scene);
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
}

void test_uniform_ring_blocks_lower_hemisphere() {
  SceneRaycaster scene;

  // 北側の壁
  scene.add_box({0.0, 10.0, 2.5}, {50.0, 1.0, 5.0}, {0.0, 0.0, 0.0});
  // 南側の壁
  scene.add_box({0.0, -10.0, 2.5}, {50.0, 1.0, 5.0}, {0.0, 0.0, 0.0});
  // // 東側の壁
  scene.add_box({10.0, 0.0, 2.5}, {1.0, 50.0, 5.0}, {0.0, 0.0, 0.0});
  // 西側の壁
  scene.add_box({-10.0, 0.0, 2.5}, {1.0, 50.0, 5.0}, {0.0, 0.0, 0.0});

  SkyRatioChecker checker;
  checker.ray_resolution = 1.;
  checker.checkpoints.push_back({0.0, 0.0, 0}); // 原点付近

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  auto sky_ratios = checker.check(&scene);
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
  scene.save("test.stl");
}

void test_totally_enclosed() {
  SceneRaycaster scene;
  scene.add_box({0.0, 0.0, 5.0}, {10.0, 10.0, 10.0}, {0.0, 0.0, 0.0}); // 大きな箱で完全に囲む
  scene.build();

  SkyRatioChecker checker;
  checker.ray_resolution = 5.0f;                  // 5度刻み
  checker.checkpoints.push_back({0.0, 0.0, 1.5}); // 原点付近

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  auto sky_ratios = checker.check(&scene);
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
}

int main() {
  // test_no_obstacles();
  // test_large_wall_blocks_half_hemisphere();
  // test_many_small_objects_far_away();
  test_uniform_ring_blocks_lower_hemisphere();

  // // シーンの作成
  // SceneRaycaster scene;

  // // 建物を追加(ボックス)
  // scene.add_box({5.0, 0.0, 0.0}, {2.0, 2.0, 10.0}, {0.0, 0.0, 0.0});
  // scene.add_box({-5.0, 0.0, 0.0}, {2.0, 2.0, 8.0}, {0.0, 0.0, 0.0});

  // // 球体を追加
  // scene.add_sphere({0.0, 8.0, 5.0}, 2.0);

  // // BVHをビルド
  // scene.build();
  // std::cout << "シーンを構築しました" << std::endl;

  // // 天空率チェッカーの作成
  // SkyRatioChecker checker;
  // checker.set_scene(scene);
  // checker.ray_resolution = 5.0f; // 5度刻み

  // // 測定点を追加
  // checker.checkpoints.push_back({0.0, 0.0, 1.5});  // 原点付近
  // checker.checkpoints.push_back({3.0, 0.0, 1.5});  // 建物に近い位置
  // checker.checkpoints.push_back({10.0, 0.0, 1.5}); // 離れた位置

  // std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  // std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  // // 天空率を計算
  // std::cout << "\n天空率を計算中..." << std::endl;
  // auto sky_ratios = checker.check();

  // // 結果を表示
  // std::cout << "\n=== 計算結果 ===" << std::endl;
  // for(size_t i = 0; i < sky_ratios.size(); i++) {
  //   const auto& cp = checker.checkpoints[i];
  //   std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  // }

  return 0;
}
