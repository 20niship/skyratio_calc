"""
C++実装と純粋なPython実装の性能を比較するベンチマークスクリプト

testディレクトリから実行してください:
    cd test && python benchmark.py

ベンチマークグラフは親ディレクトリ（リポジトリルート）に保存されます。
"""

import time
import os
import matplotlib.pyplot as plt
import numpy as np
import skyratio_calc
from python_implementation import SceneRaycasterPython, SkyRatioCheckerPython


# 出力ディレクトリを親ディレクトリ（リポジトリルート）に設定
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..")


def benchmark_cpp(num_boxes: int, num_checkpoints: int, ray_resolution: float = 5.0) -> float:
    """
    C++実装のベンチマーク
    戻り値: 実行時間（秒）
    """
    # ボックスを持つシーンを作成
    scene = skyratio_calc.SceneRaycaster()

    for i in range(num_boxes):
        # 異なる位置にボックスを追加
        x = (i % 5) * 5.0 - 10.0
        y = (i // 5) * 5.0 - 10.0
        scene.add_box([x, y, 5.0], [2.0, 2.0, 4.0], [0.0, 0.0, 0.0])

    scene.build()

    # 複数の測定点を持つチェッカーを作成
    checker = skyratio_calc.SkyRatioChecker()
    checker.set_scene(scene)
    checker.ray_resolution = ray_resolution

    # 測定点を生成
    checkpoints = []
    for i in range(num_checkpoints):
        x = (i % 10) * 2.0 - 10.0
        y = (i // 10) * 2.0 - 10.0
        checkpoints.append([x, y, 1.5])

    checker.checkpoints = checkpoints

    # 時間を計測（結果の値は使用せず、実行時間のみを測定）
    start_time = time.time()
    _ = checker.check()
    end_time = time.time()

    return end_time - start_time


def benchmark_python(num_boxes: int, num_checkpoints: int, ray_resolution: float = 5.0) -> float:
    """
    純粋なPython実装のベンチマーク
    戻り値: 実行時間（秒）
    """
    # ボックスを持つシーンを作成
    scene = SceneRaycasterPython()

    for i in range(num_boxes):
        # 異なる位置にボックスを追加
        x = (i % 5) * 5.0 - 10.0
        y = (i // 5) * 5.0 - 10.0
        scene.add_box([x, y, 5.0], [2.0, 2.0, 4.0], [0.0, 0.0, 0.0])

    scene.build()

    # 複数の測定点を持つチェッカーを作成
    checker = SkyRatioCheckerPython()
    checker.set_scene(scene)
    checker.ray_resolution = ray_resolution

    # 測定点を生成
    checkpoints = []
    for i in range(num_checkpoints):
        x = (i % 10) * 2.0 - 10.0
        y = (i // 10) * 2.0 - 10.0
        checkpoints.append([x, y, 1.5])

    checker.checkpoints = checkpoints

    # 時間を計測（結果の値は使用せず、実行時間のみを測定）
    start_time = time.time()
    _ = checker.check()
    end_time = time.time()

    return end_time - start_time


def benchmark_comparison_1():
    """
    比較1: 長方形の数（1〜10個）と計算時間
    固定値: 測定点100個、ray_resolution = 10.0度
    """
    print("=== ベンチマーク1: 長方形の数と計算時間 ===")

    num_boxes_list = list(range(1, 11))
    num_checkpoints = 100
    ray_resolution = 10.0

    cpp_times = []
    python_times = []

    for num_boxes in num_boxes_list:
        print(f"{num_boxes}個のボックスでテスト中...")

        # C++ベンチマーク
        cpp_time = benchmark_cpp(num_boxes, num_checkpoints, ray_resolution)
        cpp_times.append(cpp_time)
        print(f"  C++時間: {cpp_time:.4f}秒")

        # Pythonベンチマーク
        python_time = benchmark_python(num_boxes, num_checkpoints, ray_resolution)
        python_times.append(python_time)
        print(f"  Python時間: {python_time:.4f}秒")
        print(f"  高速化倍率: {python_time / cpp_time:.2f}x")
        print()

    # 結果をプロット
    plt.figure(figsize=(10, 6))
    plt.plot(num_boxes_list, cpp_times, "o-", label="C++実装", linewidth=2, markersize=8)
    plt.plot(num_boxes_list, python_times, "s-", label="純粋なPython実装", linewidth=2, markersize=8)
    plt.xlabel("長方形の数", fontsize=12)
    plt.ylabel("計算時間（秒）", fontsize=12)
    plt.title("パフォーマンス比較: 長方形の数と計算時間\n（測定点100個、解像度10°）", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "benchmark_rectangles.png")
    plt.savefig(output_path, dpi=150)
    print(f"グラフを保存しました: {output_path}")

    return num_boxes_list, cpp_times, python_times


def benchmark_comparison_2():
    """
    比較2: 測定点の数（10〜300個）と計算時間
    固定値: 長方形5個、ray_resolution = 10.0度
    """
    print("\n=== ベンチマーク2: 測定点の数と計算時間 ===")

    num_checkpoints_list = [10, 30, 50, 70, 100, 150, 200, 250, 300]
    num_boxes = 5
    ray_resolution = 10.0

    cpp_times = []
    python_times = []

    for num_checkpoints in num_checkpoints_list:
        print(f"{num_checkpoints}個の測定点でテスト中...")

        # C++ベンチマーク
        cpp_time = benchmark_cpp(num_boxes, num_checkpoints, ray_resolution)
        cpp_times.append(cpp_time)
        print(f"  C++時間: {cpp_time:.4f}秒")

        # Pythonベンチマーク
        python_time = benchmark_python(num_boxes, num_checkpoints, ray_resolution)
        python_times.append(python_time)
        print(f"  Python時間: {python_time:.4f}秒")
        print(f"  高速化倍率: {python_time / cpp_time:.2f}x")
        print()

    # 結果をプロット
    plt.figure(figsize=(10, 6))
    plt.plot(num_checkpoints_list, cpp_times, "o-", label="C++実装", linewidth=2, markersize=8)
    plt.plot(num_checkpoints_list, python_times, "s-", label="純粋なPython実装", linewidth=2, markersize=8)
    plt.xlabel("測定点の数", fontsize=12)
    plt.ylabel("計算時間（秒）", fontsize=12)
    plt.title("パフォーマンス比較: 測定点の数と計算時間\n（長方形5個、解像度10°）", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "benchmark_checkpoints.png")
    plt.savefig(output_path, dpi=150)
    print(f"グラフを保存しました: {output_path}")

    return num_checkpoints_list, cpp_times, python_times


def print_summary(boxes_data, checkpoints_data):
    """サマリー統計を出力"""
    print("\n" + "=" * 70)
    print("ベンチマーク結果サマリー")
    print("=" * 70)

    num_boxes_list, cpp_times_1, python_times_1 = boxes_data
    num_checkpoints_list, cpp_times_2, python_times_2 = checkpoints_data

    # ベンチマーク1のサマリー
    avg_speedup_1 = np.mean([p / c for p, c in zip(python_times_1, cpp_times_1)])
    print("\nベンチマーク1（長方形の数を変化）:")
    print(f"  平均C++時間: {np.mean(cpp_times_1):.4f}秒")
    print(f"  平均Python時間: {np.mean(python_times_1):.4f}秒")
    print(f"  平均高速化倍率（Python/C++）: {avg_speedup_1:.2f}x")

    # ベンチマーク2のサマリー
    avg_speedup_2 = np.mean([p / c for p, c in zip(python_times_2, cpp_times_2)])
    print("\nベンチマーク2（測定点の数を変化）:")
    print(f"  平均C++時間: {np.mean(cpp_times_2):.4f}秒")
    print(f"  平均Python時間: {np.mean(python_times_2):.4f}秒")
    print(f"  平均高速化倍率（Python/C++）: {avg_speedup_2:.2f}x")

    print("\n" + "=" * 70)


def generate_markdown_tables(boxes_data, checkpoints_data):
    """Markdown形式の表を生成してREADME用のテキストを返す"""
    num_boxes_list, cpp_times_1, python_times_1 = boxes_data
    num_checkpoints_list, cpp_times_2, python_times_2 = checkpoints_data

    # ベンチマーク1の表
    table1 = "\n### ベンチマーク1: 長方形の数と計算時間\n\n"
    table1 += "| 長方形の数 | C++実装 (秒) | Python実装 (秒) | 高速化倍率 |\n"
    table1 += "|-----------|-------------|----------------|----------|\n"
    for i, num_boxes in enumerate(num_boxes_list):
        speedup = python_times_1[i] / cpp_times_1[i]
        table1 += f"| {num_boxes} | {cpp_times_1[i]:.4f} | {python_times_1[i]:.4f} | {speedup:.2f}x |\n"

    avg_speedup_1 = np.mean([p / c for p, c in zip(python_times_1, cpp_times_1)])
    table1 += f"\n**平均高速化倍率**: {avg_speedup_1:.2f}x\n"

    # ベンチマーク2の表
    table2 = "\n### ベンチマーク2: 測定点の数と計算時間\n\n"
    table2 += "| 測定点の数 | C++実装 (秒) | Python実装 (秒) | 高速化倍率 |\n"
    table2 += "|-----------|-------------|----------------|----------|\n"
    for i, num_checkpoints in enumerate(num_checkpoints_list):
        speedup = python_times_2[i] / cpp_times_2[i]
        table2 += f"| {num_checkpoints} | {cpp_times_2[i]:.4f} | {python_times_2[i]:.4f} | {speedup:.2f}x |\n"

    avg_speedup_2 = np.mean([p / c for p, c in zip(python_times_2, cpp_times_2)])
    table2 += f"\n**平均高速化倍率**: {avg_speedup_2:.2f}x\n"

    return table1 + table2


def main():
    print("天空率計算 - パフォーマンスベンチマーク")
    print("=" * 70)
    print()

    # ベンチマークを実行
    boxes_data = benchmark_comparison_1()
    checkpoints_data = benchmark_comparison_2()

    # サマリーを出力
    print_summary(boxes_data, checkpoints_data)

    # Markdown表を生成して表示
    markdown_tables = generate_markdown_tables(boxes_data, checkpoints_data)
    print("\n" + "=" * 70)
    print("README用のMarkdown表:")
    print("=" * 70)
    print(markdown_tables)


if __name__ == "__main__":
    main()
