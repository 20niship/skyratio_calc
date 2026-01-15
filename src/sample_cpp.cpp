#include "scene_raycaster.hpp"
#include "sky_ratio_checker.hpp"
#include <iomanip>
#include <iostream>

void test_no_obstacles() {
  std::cout << "=== 天空率計算サンプル ===" << std::endl;
  SceneRaycaster scene;
  SkyRatioChecker checker;
  checker.ray_resolution = 10.0f;                 // 10度刻み
  checker.checkpoints.push_back({0.0, 0.0, 1.5}); // 原点付近

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  std::cout << "\n天空率を計算中..." << std::endl;
  auto sky_ratios = checker.check(&scene);
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
}

void test_large_wall_blocks_half_hemisphere() {
  std::cout << "=== 天空率計算サンプル ===" << std::endl;
  SceneRaycaster scene;
  scene.add_box({0.0, 2.0, 50.0}, {100.0, 1.0, 100.0}, {0.0, 0.0, 0.0});
  SkyRatioChecker checker;
  checker.ray_resolution = 5.0f;                  // 5度刻み
  checker.checkpoints.push_back({0.0, 0.0, 1.5}); // 原点付近

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  std::cout << "\n天空率を計算中..." << std::endl;
  auto sky_ratios = checker.check(&scene);
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
}

void test_many_small_objects_far_away() {
  std::cout << "=== 天空率計算サンプル ===" << std::endl;
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

  std::cout << "\n天空率を計算中..." << std::endl;
  auto sky_ratios = checker.check(&scene);
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
}

void test_uniform_ring_blocks_lower_hemisphere() {
  std::cout << "=== 天空率計算サンプル ===" << std::endl;
  SceneRaycaster scene;

  // 北側の壁
  scene.add_box({0.0, 10.0, 2.5}, {50.0, 1.0, 5.0}, {0.0, 0.0, 0.0});
  // 南側の壁
  scene.add_box({0.0, -10.0, 2.5}, {50.0, 1.0, 5.0}, {0.0, 0.0, 0.0});
  // 東側の壁
  scene.add_box({10.0, 0.0, 2.5}, {1.0, 50.0, 5.0}, {0.0, 0.0, 0.0});
  // 西側の壁
  scene.add_box({-10.0, 0.0, 2.5}, {1.0, 50.0, 5.0}, {0.0, 0.0, 0.0});

  SkyRatioChecker checker;
  checker.ray_resolution = 5.0f;                  // 5度刻み
  checker.checkpoints.push_back({0.0, 0.0, 1.5}); // 原点付近

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  std::cout << "\n天空率を計算中..." << std::endl;
  auto sky_ratios = checker.check(&scene);
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
}

void test_totally_enclosed() {
  std::cout << "=== 天空率計算サンプル ===" << std::endl;
  SceneRaycaster scene;
  scene.add_box({0.0, 0.0, 5.0}, {10.0, 10.0, 10.0}, {0.0, 0.0, 0.0}); // 大きな箱で完全に囲む
  scene.build();

  SkyRatioChecker checker;
  checker.ray_resolution = 5.0f;                  // 5度刻み
  checker.checkpoints.push_back({0.0, 0.0, 1.5}); // 原点付近

  std::cout << "測定点数: " << checker.checkpoints.size() << std::endl;
  std::cout << "レイの刻み: " << checker.ray_resolution << "度" << std::endl;

  std::cout << "\n天空率を計算中..." << std::endl;
  auto sky_ratios = checker.check(&scene);
  std::cout << "\n=== 計算結果 ===" << std::endl;
  for(size_t i = 0; i < sky_ratios.size(); i++) {
    const auto& cp = checker.checkpoints[i];
    std::cout << "測定点 " << i + 1 << " (" << std::fixed << std::setprecision(1) << cp[0] << ", " << cp[1] << ", " << cp[2] << "): " << std::setprecision(2) << (sky_ratios[i] * 100.0f) << "%" << std::endl;
  }
}

int main() {
  std::cout << "=== 天空率計算サンプル ===" << std::endl;

  test_no_obstacles();
  test_large_wall_blocks_half_hemisphere();
  test_many_small_objects_far_away();
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

// """
// 天空率の積分計算のテスト
// 正射影面積を用いた計算が正しく動作することを確認
// """
// import skyratio_calc
// import math


// def test_large_wall_blocks_half_hemisphere():
//     """
//     テスト1: 非常に大きい壁が半球の約半分を遮るケース

//     大きな壁の直ぐ側に測定点を置くと、空のうちほぼ半球が隠れるため、
//     天空率は50％前後となることを確認
//     """
//     scene = skyratio_calc.SceneRaycaster()

//     # 非常に大きな壁を作成（高さ100m、幅100m、厚さ1m）
//     # 測定点のすぐ北側（y方向正）に配置
//     # 壁の下端が地面（z=0）、上端がz=100になるように配置
//     scene.add_box([0.0, 2.0, 50.0], [100.0, 1.0, 100.0], [0.0, 0.0, 0.0])
//     scene.build()

//     checker = skyratio_calc.SkyRatioChecker()
//     checker.set_scene(scene)
//     checker.ray_resolution = 5.0  # 5度刻み

//     # 壁の直ぐ側（y=0、高さ1.5m）に測定点を配置
//     checker.checkpoints = [[0.0, 0.0, 1.5]]

//     sky_ratios = checker.check()

//     assert len(sky_ratios) == 1, "測定点は1つ"
//     sky_ratio = sky_ratios[0]

//     # 壁が北側の半球をほぼ完全に遮るため、天空率は約50%前後
//     # 実際には壁の端から少し空が見えるので、45-55%の範囲を許容
//     print(f"大きな壁テスト: 天空率 {sky_ratio * 100:.2f}%")
//     assert 0.45 < sky_ratio < 0.55, \
//         f"大きな壁が半球を遮る場合、天空率は45-55%の範囲のはずが {sky_ratio * 100:.2f}%"

//     print("✓ 大きな壁が半球の約半分を遮るケース: PASS")


// def test_many_small_objects_far_away():
//     """
//     テスト2: 小さなオブジェクトが多数あるが、測定点が十分離れているケース

//     小さめのオブジェクトが数十個並んでいて、測定点が十分に離れているときは、
//     天空率は高い値（90%以上）になることを確認
//     """
//     scene = skyratio_calc.SceneRaycaster()

//     # 小さなボックス（1m x 1m x 1m）を40個、測定点から離して配置
//     num_boxes = 40
//     radius = 50.0  # 測定点から50m離れた円周上に配置

//     for i in range(num_boxes):
//         angle = 2.0 * math.pi * i / num_boxes
//         x = radius * math.cos(angle)
//         y = radius * math.sin(angle)
//         z = 5.0  # 地面より少し上
//         scene.add_box([x, y, z], [1.0, 1.0, 1.0], [0.0, 0.0, 0.0])

//     scene.build()

//     checker = skyratio_calc.SkyRatioChecker()
//     checker.set_scene(scene)
//     checker.ray_resolution = 5.0  # 5度刻み

//     # 原点に測定点を配置
//     checker.checkpoints = [[0.0, 0.0, 1.5]]

//     sky_ratios = checker.check()

//     assert len(sky_ratios) == 1, "測定点は1つ"
//     sky_ratio = sky_ratios[0]

//     # 小さなオブジェクトが遠くにあるため、天空率は高いはず（90%以上）
//     print(f"小さなオブジェクト遠方テスト: 天空率 {sky_ratio * 100:.2f}%")
//     assert sky_ratio > 0.90, \
//         f"小さなオブジェクトが遠くにある場合、天空率は90%以上のはずが {sky_ratio * 100:.2f}%"

//     print("✓ 小さなオブジェクトが遠くにあるケース: PASS")


// def test_uniform_ring_blocks_lower_hemisphere():
//     """
//     テスト3: 等間隔の直方体で天球の下部を一定割合遮るケース

//     直方体を測定点から同じ距離で等間隔に並べて、天球の下の方の
//     一定割合を360度ビルで遮った場合、それに従うような天空率になることを確認
//     """
//     scene = skyratio_calc.SceneRaycaster()

//     # より簡単なテスト: 4方向に大きな壁を配置
//     # 測定点から10m離れた位置に、高さ5mの壁を4方向に配置
//     radius = 10.0
//     wall_height = 5.0
//     wall_size = 50.0  # 壁の幅と奥行き

//     # 北側の壁
//     scene.add_box([0.0, radius, wall_height / 2.0], [wall_size, 1.0, wall_height], [0.0, 0.0, 0.0])
//     # 南側の壁
//     scene.add_box([0.0, -radius, wall_height / 2.0], [wall_size, 1.0, wall_height], [0.0, 0.0, 0.0])
//     # 東側の壁
//     scene.add_box([radius, 0.0, wall_height / 2.0], [1.0, wall_size, wall_height], [0.0, 0.0, 0.0])
//     # 西側の壁
//     scene.add_box([-radius, 0.0, wall_height / 2.0], [1.0, wall_size, wall_height], [0.0, 0.0, 0.0])

//     scene.build()

//     checker = skyratio_calc.SkyRatioChecker()
//     checker.set_scene(scene)
//     checker.ray_resolution = 5.0  # 5度刻み

//     # 原点（壁に囲まれた中心）に測定点を配置
//     checker.checkpoints = [[0.0, 0.0, 1.5]]

//     sky_ratios = checker.check()

//     assert len(sky_ratios) == 1, "測定点は1つ"
//     sky_ratio = sky_ratios[0]

//     # 理論計算: 壁の上端が見える天頂角θを計算
//     # tan(θ) = radius / (wall_height - checkpoint_z)
//     checkpoint_z = 1.5
//     wall_top = wall_height
//     theta_max = math.atan2(radius, wall_top - checkpoint_z)

//     # 天頂角θ_maxまでが遮られている
//     # 正射影面積: π * sin²(θ_max)
//     blocked_area = math.pi * (math.sin(theta_max) ** 2)
//     total_area = math.pi
//     expected_sky_ratio = 1.0 - (blocked_area / total_area)

//     print(f"等間隔リングテスト: 天空率 {sky_ratio * 100:.2f}%")
//     print(f"  理論値（完全な円の場合）: {expected_sky_ratio * 100:.2f}%")
//     print(f"  theta_max: {math.degrees(theta_max):.1f}度")
//     print(f"  差分: {abs(sky_ratio - expected_sky_ratio) * 100:.2f}%")

//     # 4方向の壁なので完全な円ではないが、ある程度は遮られるはず
//     # 三斜求積法では20-89度の範囲でレイを飛ばすため、
//     # 4つの壁が低い角度で天空を遮る
//     # 天空率が50-70%の範囲内であることを確認
//     assert 0.50 < sky_ratio < 0.70, \
//         f"4方向の壁がある場合、天空率は50-70%の範囲のはずが {sky_ratio * 100:.2f}%"

//     print("✓ 等間隔リングで下部を遮るケース: PASS")


// def test_no_obstacles():
//     """
//     テスト4: 障害物がない場合、天空率は100%
//     """
//     scene = skyratio_calc.SceneRaycaster()
//     scene.build()  # 空のシーン

//     checker = skyratio_calc.SkyRatioChecker()
//     checker.set_scene(scene)
//     checker.ray_resolution = 10.0  # 10度刻み
//     checker.checkpoints = [[0.0, 0.0, 1.5]]

//     sky_ratios = checker.check()

//     assert len(sky_ratios) == 1
//     sky_ratio = sky_ratios[0]

//     print(f"障害物なしテスト: 天空率 {sky_ratio * 100:.2f}%")
//     assert abs(sky_ratio - 1.0) < 0.01, \
//         f"障害物がない場合、天空率は100%のはずが {sky_ratio * 100:.2f}%"

//     print("✓ 障害物なしケース: PASS")


// def test_completely_enclosed():
//     """
//     テスト5: 上に大きな障害物がある場合、天空率は低い
//     """
//     scene = skyratio_calc.SceneRaycaster()

//     # 測定点の真上に大きな天井を配置
//     # 測定点から3m上（z=4.5）に大きな厚い天井
//     scene.add_box([0.0, 0.0, 5.0], [100.0, 100.0, 2.0], [0.0, 0.0, 0.0])
//     scene.build()

//     checker = skyratio_calc.SkyRatioChecker()
//     checker.set_scene(scene)
//     checker.ray_resolution = 10.0  # 10度刻み
//     checker.checkpoints = [[0.0, 0.0, 1.5]]

//     sky_ratios = checker.check()

//     assert len(sky_ratios) == 1
//     sky_ratio = sky_ratios[0]

//     print(f"天井ありテスト: 天空率 {sky_ratio * 100:.2f}%")
//     # 真上に大きな天井があるので、天空率は低いはず（50%以下）
//     assert sky_ratio < 0.50, \
//         f"真上に大きな天井がある場合、天空率は50%以下のはずが {sky_ratio * 100:.2f}%"

//     print("✓ 天井があるケース: PASS")


// if __name__ == "__main__":
//     print("=== 天空率積分計算のテスト ===\n")

//     test_no_obstacles()
//     print()

//     test_large_wall_blocks_half_hemisphere()
//     print()

//     test_many_small_objects_far_away()
//     print()

//     test_uniform_ring_blocks_lower_hemisphere()
//     print()

//     test_completely_enclosed()
//     print()

//     print("=== すべてのテストが成功しました！ ===")
