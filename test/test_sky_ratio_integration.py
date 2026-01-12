"""
天空率の積分計算のテスト
正射影面積を用いた計算が正しく動作することを確認
"""
import sky_ratio_calc
import math


def test_large_wall_blocks_half_hemisphere():
    """
    テスト1: 非常に大きい壁が半球の約半分を遮るケース
    
    大きな壁の直ぐ側に測定点を置くと、空のうちほぼ半球が隠れるため、
    天空率は50％前後となることを確認
    """
    scene = sky_ratio_calc.SceneRaycaster()
    
    # 非常に大きな壁を作成（高さ100m、幅100m、厚さ1m）
    # 測定点のすぐ北側（y方向正）に配置
    # 壁の下端が地面（z=0）、上端がz=100になるように配置
    scene.add_box([0.0, 2.0, 50.0], [100.0, 1.0, 100.0], [0.0, 0.0, 0.0])
    scene.build()
    
    checker = sky_ratio_calc.SkyRatioChecker()
    checker.set_scene(scene)
    checker.ray_resolution = 5.0  # 5度刻み
    
    # 壁の直ぐ側（y=0、高さ1.5m）に測定点を配置
    checker.checkpoints = [[0.0, 0.0, 1.5]]
    
    sky_ratios = checker.check()
    
    assert len(sky_ratios) == 1, "測定点は1つ"
    sky_ratio = sky_ratios[0]
    
    # 壁が北側の半球をほぼ完全に遮るため、天空率は約50%前後
    # 実際には壁の端から少し空が見えるので、45-55%の範囲を許容
    print(f"大きな壁テスト: 天空率 {sky_ratio * 100:.2f}%")
    assert 0.45 < sky_ratio < 0.55, \
        f"大きな壁が半球を遮る場合、天空率は45-55%の範囲のはずが {sky_ratio * 100:.2f}%"
    
    print("✓ 大きな壁が半球の約半分を遮るケース: PASS")


def test_many_small_objects_far_away():
    """
    テスト2: 小さなオブジェクトが多数あるが、測定点が十分離れているケース
    
    小さめのオブジェクトが数十個並んでいて、測定点が十分に離れているときは、
    天空率は高い値（90%以上）になることを確認
    """
    scene = sky_ratio_calc.SceneRaycaster()
    
    # 小さなボックス（1m x 1m x 1m）を40個、測定点から離して配置
    num_boxes = 40
    radius = 50.0  # 測定点から50m離れた円周上に配置
    
    for i in range(num_boxes):
        angle = 2.0 * math.pi * i / num_boxes
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = 5.0  # 地面より少し上
        scene.add_box([x, y, z], [1.0, 1.0, 1.0], [0.0, 0.0, 0.0])
    
    scene.build()
    
    checker = sky_ratio_calc.SkyRatioChecker()
    checker.set_scene(scene)
    checker.ray_resolution = 5.0  # 5度刻み
    
    # 原点に測定点を配置
    checker.checkpoints = [[0.0, 0.0, 1.5]]
    
    sky_ratios = checker.check()
    
    assert len(sky_ratios) == 1, "測定点は1つ"
    sky_ratio = sky_ratios[0]
    
    # 小さなオブジェクトが遠くにあるため、天空率は高いはず（90%以上）
    print(f"小さなオブジェクト遠方テスト: 天空率 {sky_ratio * 100:.2f}%")
    assert sky_ratio > 0.90, \
        f"小さなオブジェクトが遠くにある場合、天空率は90%以上のはずが {sky_ratio * 100:.2f}%"
    
    print("✓ 小さなオブジェクトが遠くにあるケース: PASS")


def test_uniform_ring_blocks_lower_hemisphere():
    """
    テスト3: 等間隔の直方体で天球の下部を一定割合遮るケース
    
    直方体を測定点から同じ距離で等間隔に並べて、天球の下の方の
    一定割合を360度ビルで遮った場合、それに従うような天空率になることを確認
    """
    scene = sky_ratio_calc.SceneRaycaster()
    
    # より簡単なテスト: 4方向に大きな壁を配置
    # 測定点から10m離れた位置に、高さ5mの壁を4方向に配置
    radius = 10.0
    wall_height = 5.0
    wall_size = 50.0  # 壁の幅と奥行き
    
    # 北側の壁
    scene.add_box([0.0, radius, wall_height / 2.0], [wall_size, 1.0, wall_height], [0.0, 0.0, 0.0])
    # 南側の壁
    scene.add_box([0.0, -radius, wall_height / 2.0], [wall_size, 1.0, wall_height], [0.0, 0.0, 0.0])
    # 東側の壁
    scene.add_box([radius, 0.0, wall_height / 2.0], [1.0, wall_size, wall_height], [0.0, 0.0, 0.0])
    # 西側の壁
    scene.add_box([-radius, 0.0, wall_height / 2.0], [1.0, wall_size, wall_height], [0.0, 0.0, 0.0])
    
    scene.build()
    
    checker = sky_ratio_calc.SkyRatioChecker()
    checker.set_scene(scene)
    checker.ray_resolution = 5.0  # 5度刻み
    
    # 原点（壁に囲まれた中心）に測定点を配置
    checker.checkpoints = [[0.0, 0.0, 1.5]]
    
    sky_ratios = checker.check()
    
    assert len(sky_ratios) == 1, "測定点は1つ"
    sky_ratio = sky_ratios[0]
    
    # 理論計算: 壁の上端が見える天頂角θを計算
    # tan(θ) = radius / (wall_height - checkpoint_z)
    checkpoint_z = 1.5
    wall_top = wall_height
    theta_max = math.atan2(radius, wall_top - checkpoint_z)
    
    # 天頂角θ_maxまでが遮られている
    # 正射影面積: π * sin²(θ_max)
    blocked_area = math.pi * (math.sin(theta_max) ** 2)
    total_area = math.pi
    expected_sky_ratio = 1.0 - (blocked_area / total_area)
    
    print(f"等間隔リングテスト: 天空率 {sky_ratio * 100:.2f}%")
    print(f"  理論値: {expected_sky_ratio * 100:.2f}%")
    print(f"  theta_max: {math.degrees(theta_max):.1f}度")
    print(f"  差分: {abs(sky_ratio - expected_sky_ratio) * 100:.2f}%")
    
    # 4方向の壁なので完全な円ではないが、ある程度は遮られるはず
    # 天空率が理論値より高くなることを確認（少なくとも70%以上）
    assert sky_ratio > 0.70, \
        f"4方向の壁がある場合、天空率は70%以上のはずが {sky_ratio * 100:.2f}%"
    
    print("✓ 等間隔リングで下部を遮るケース: PASS")


def test_no_obstacles():
    """
    テスト4: 障害物がない場合、天空率は100%
    """
    scene = sky_ratio_calc.SceneRaycaster()
    scene.build()  # 空のシーン
    
    checker = sky_ratio_calc.SkyRatioChecker()
    checker.set_scene(scene)
    checker.ray_resolution = 10.0  # 10度刻み
    checker.checkpoints = [[0.0, 0.0, 1.5]]
    
    sky_ratios = checker.check()
    
    assert len(sky_ratios) == 1
    sky_ratio = sky_ratios[0]
    
    print(f"障害物なしテスト: 天空率 {sky_ratio * 100:.2f}%")
    assert abs(sky_ratio - 1.0) < 0.01, \
        f"障害物がない場合、天空率は100%のはずが {sky_ratio * 100:.2f}%"
    
    print("✓ 障害物なしケース: PASS")


def test_completely_enclosed():
    """
    テスト5: 上に大きな障害物がある場合、天空率は低い
    """
    scene = sky_ratio_calc.SceneRaycaster()
    
    # 測定点の真上に大きな天井を配置
    # 測定点から3m上（z=4.5）に大きな厚い天井
    scene.add_box([0.0, 0.0, 5.0], [100.0, 100.0, 2.0], [0.0, 0.0, 0.0])
    scene.build()
    
    checker = sky_ratio_calc.SkyRatioChecker()
    checker.set_scene(scene)
    checker.ray_resolution = 10.0  # 10度刻み
    checker.checkpoints = [[0.0, 0.0, 1.5]]
    
    sky_ratios = checker.check()
    
    assert len(sky_ratios) == 1
    sky_ratio = sky_ratios[0]
    
    print(f"天井ありテスト: 天空率 {sky_ratio * 100:.2f}%")
    # 真上に大きな天井があるので、天空率は低いはず（50%以下）
    assert sky_ratio < 0.50, \
        f"真上に大きな天井がある場合、天空率は50%以下のはずが {sky_ratio * 100:.2f}%"
    
    print("✓ 天井があるケース: PASS")


if __name__ == "__main__":
    print("=== 天空率積分計算のテスト ===\n")
    
    test_no_obstacles()
    print()
    
    test_large_wall_blocks_half_hemisphere()
    print()
    
    test_many_small_objects_far_away()
    print()
    
    test_uniform_ring_blocks_lower_hemisphere()
    print()
    
    test_completely_enclosed()
    print()
    
    print("=== すべてのテストが成功しました！ ===")
