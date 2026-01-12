"""
C++バインディングのテスト
"""
import sky_ratio_calc


def test_scene_raycaster():
    """SceneRaycasterのテスト"""
    scene = sky_ratio_calc.SceneRaycaster()
    
    # ボックスと球体を追加
    scene.add_box([0.0, 0.0, 5.0], [2.0, 2.0, 2.0], [0.0, 0.0, 0.0])
    scene.add_sphere([0.0, 0.0, -5.0], 1.0)
    scene.build()
    
    # レイキャスト実行
    origins = [[0.0, 0.0, 0.0]]
    directions = [[0.0, 0.0, 1.0]]  # 上方向
    results = scene.raycast(origins, directions)
    
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"
    assert results[0].hit, "Expected hit"
    print(f"✓ SceneRaycaster: ヒット距離 {results[0].distance:.2f}")


def test_sky_ratio_checker():
    """SkyRatioCheckerのテスト"""
    scene = sky_ratio_calc.SceneRaycaster()
    scene.add_box([0.0, 0.0, 10.0], [5.0, 5.0, 2.0], [0.0, 0.0, 0.0])
    scene.build()
    
    checker = sky_ratio_calc.SkyRatioChecker()
    checker.set_scene(scene)
    checker.ray_resolution = 10.0
    checker.checkpoints = [[0.0, 0.0, 1.5]]
    
    sky_ratios = checker.check()
    
    assert len(sky_ratios) == 1, f"Expected 1 result, got {len(sky_ratios)}"
    assert 0.0 <= sky_ratios[0] <= 1.0, f"Sky ratio should be between 0 and 1, got {sky_ratios[0]}"
    print(f"✓ SkyRatioChecker: 天空率 {sky_ratios[0] * 100:.2f}%")


if __name__ == "__main__":
    test_scene_raycaster()
    test_sky_ratio_checker()
    print("\nすべてのテストが成功しました！")
