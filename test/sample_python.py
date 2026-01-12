"""
天空率計算のPythonサンプル
"""
import sky_ratio_calc

def main():
    print("=== 天空率計算サンプル (Python) ===\n")
    
    # シーンの作成
    scene = sky_ratio_calc.SceneRaycaster()
    
    # 建物を追加(ボックス)
    scene.add_box([5.0, 0.0, 0.0], [2.0, 2.0, 10.0], [0.0, 0.0, 0.0])
    scene.add_box([-5.0, 0.0, 0.0], [2.0, 2.0, 8.0], [0.0, 0.0, 0.0])
    
    # 球体を追加
    scene.add_sphere([0.0, 8.0, 5.0], 2.0)
    
    # BVHをビルド
    scene.build()
    print("シーンを構築しました")
    
    # 天空率チェッカーの作成
    checker = sky_ratio_calc.SkyRatioChecker()
    checker.set_scene(scene)
    checker.ray_resolution = 5.0  # 5度刻み
    
    # 測定点を追加
    checker.checkpoints = [
        [0.0, 0.0, 1.5],   # 原点付近
        [3.0, 0.0, 1.5],   # 建物に近い位置
        [10.0, 0.0, 1.5],  # 離れた位置
    ]
    
    print(f"測定点数: {len(checker.checkpoints)}")
    print(f"レイの刻み: {checker.ray_resolution}度")
    
    # 天空率を計算
    print("\n天空率を計算中...")
    sky_ratios = checker.check()
    
    # 結果を表示
    print("\n=== 計算結果 ===")
    for i, (checkpoint, ratio) in enumerate(zip(checker.checkpoints, sky_ratios)):
        print(f"測定点 {i + 1} ({checkpoint[0]:.1f}, {checkpoint[1]:.1f}, {checkpoint[2]:.1f}): {ratio * 100:.2f}%")
    
    print("\n=== レイキャストの直接テスト ===")
    # レイキャストの直接テスト
    origins = [[0.0, 0.0, 1.5]]
    directions = [[0.0, 0.0, 1.0]]  # 真上
    results = scene.raycast(origins, directions)
    
    if results[0].hit:
        print(f"ヒット: 距離 {results[0].distance:.2f}, 位置 {results[0].position}")
    else:
        print("ヒットなし(天空が見えている)")

if __name__ == "__main__":
    main()
