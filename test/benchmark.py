"""
Benchmark script to compare C++ and pure Python implementations

Run this script from the test directory:
    cd test && python benchmark.py
    
The benchmark graphs will be saved in the parent directory (repository root).
"""
import time
import os
import matplotlib.pyplot as plt
import numpy as np
import sky_ratio_calc
from python_implementation import SceneRaycasterPython, SkyRatioCheckerPython


# Set output directory to parent directory (repository root)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..')


def benchmark_cpp(num_boxes: int, num_checkpoints: int, ray_resolution: float = 5.0) -> float:
    """
    Benchmark C++ implementation
    Returns: execution time in seconds
    """
    # Create scene with boxes
    scene = sky_ratio_calc.SceneRaycaster()
    
    for i in range(num_boxes):
        # Add boxes at different positions
        x = (i % 5) * 5.0 - 10.0
        y = (i // 5) * 5.0 - 10.0
        scene.add_box([x, y, 5.0], [2.0, 2.0, 4.0], [0.0, 0.0, 0.0])
    
    scene.build()
    
    # Create checker with multiple checkpoints
    checker = sky_ratio_calc.SkyRatioChecker()
    checker.set_scene(scene)
    checker.ray_resolution = ray_resolution
    
    # Generate checkpoints
    checkpoints = []
    for i in range(num_checkpoints):
        x = (i % 10) * 2.0 - 10.0
        y = (i // 10) * 2.0 - 10.0
        checkpoints.append([x, y, 1.5])
    
    checker.checkpoints = checkpoints
    
    # Measure time
    start_time = time.time()
    sky_ratios = checker.check()
    end_time = time.time()
    
    return end_time - start_time


def benchmark_python(num_boxes: int, num_checkpoints: int, ray_resolution: float = 5.0) -> float:
    """
    Benchmark pure Python implementation
    Returns: execution time in seconds
    """
    # Create scene with boxes
    scene = SceneRaycasterPython()
    
    for i in range(num_boxes):
        # Add boxes at different positions
        x = (i % 5) * 5.0 - 10.0
        y = (i // 5) * 5.0 - 10.0
        scene.add_box([x, y, 5.0], [2.0, 2.0, 4.0], [0.0, 0.0, 0.0])
    
    scene.build()
    
    # Create checker with multiple checkpoints
    checker = SkyRatioCheckerPython()
    checker.set_scene(scene)
    checker.ray_resolution = ray_resolution
    
    # Generate checkpoints
    checkpoints = []
    for i in range(num_checkpoints):
        x = (i % 10) * 2.0 - 10.0
        y = (i // 10) * 2.0 - 10.0
        checkpoints.append([x, y, 1.5])
    
    checker.checkpoints = checkpoints
    
    # Measure time
    start_time = time.time()
    sky_ratios = checker.check()
    end_time = time.time()
    
    return end_time - start_time


def benchmark_comparison_1():
    """
    Comparison 1: Number of rectangles (1-10) vs computation time
    Fixed: 100 checkpoints, ray_resolution = 10.0 degrees
    """
    print("=== Benchmark 1: Number of rectangles vs computation time ===")
    
    num_boxes_list = list(range(1, 11))
    num_checkpoints = 100
    ray_resolution = 10.0
    
    cpp_times = []
    python_times = []
    
    for num_boxes in num_boxes_list:
        print(f"Testing with {num_boxes} boxes...")
        
        # C++ benchmark
        cpp_time = benchmark_cpp(num_boxes, num_checkpoints, ray_resolution)
        cpp_times.append(cpp_time)
        print(f"  C++ time: {cpp_time:.4f} seconds")
        
        # Python benchmark
        python_time = benchmark_python(num_boxes, num_checkpoints, ray_resolution)
        python_times.append(python_time)
        print(f"  Python time: {python_time:.4f} seconds")
        print(f"  Speedup: {python_time / cpp_time:.2f}x")
        print()
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(num_boxes_list, cpp_times, 'o-', label='C++ Implementation', linewidth=2, markersize=8)
    plt.plot(num_boxes_list, python_times, 's-', label='Pure Python Implementation', linewidth=2, markersize=8)
    plt.xlabel('Number of Rectangles', fontsize=12)
    plt.ylabel('Computation Time (seconds)', fontsize=12)
    plt.title('Performance Comparison: Number of Rectangles vs Computation Time\n(100 checkpoints, 10° resolution)', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'benchmark_rectangles.png')
    plt.savefig(output_path, dpi=150)
    print(f"Saved graph to {output_path}")
    
    return num_boxes_list, cpp_times, python_times


def benchmark_comparison_2():
    """
    Comparison 2: Number of measurement points (10-300) vs computation time
    Fixed: 5 rectangles, ray_resolution = 10.0 degrees
    """
    print("\n=== Benchmark 2: Number of measurement points vs computation time ===")
    
    num_checkpoints_list = [10, 30, 50, 70, 100, 150, 200, 250, 300]
    num_boxes = 5
    ray_resolution = 10.0
    
    cpp_times = []
    python_times = []
    
    for num_checkpoints in num_checkpoints_list:
        print(f"Testing with {num_checkpoints} checkpoints...")
        
        # C++ benchmark
        cpp_time = benchmark_cpp(num_boxes, num_checkpoints, ray_resolution)
        cpp_times.append(cpp_time)
        print(f"  C++ time: {cpp_time:.4f} seconds")
        
        # Python benchmark
        python_time = benchmark_python(num_boxes, num_checkpoints, ray_resolution)
        python_times.append(python_time)
        print(f"  Python time: {python_time:.4f} seconds")
        print(f"  Speedup: {python_time / cpp_time:.2f}x")
        print()
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(num_checkpoints_list, cpp_times, 'o-', label='C++ Implementation', linewidth=2, markersize=8)
    plt.plot(num_checkpoints_list, python_times, 's-', label='Pure Python Implementation', linewidth=2, markersize=8)
    plt.xlabel('Number of Measurement Points', fontsize=12)
    plt.ylabel('Computation Time (seconds)', fontsize=12)
    plt.title('Performance Comparison: Number of Measurement Points vs Computation Time\n(5 rectangles, 10° resolution)', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'benchmark_checkpoints.png')
    plt.savefig(output_path, dpi=150)
    print(f"Saved graph to {output_path}")
    
    return num_checkpoints_list, cpp_times, python_times


def print_summary(boxes_data, checkpoints_data):
    """Print summary statistics"""
    print("\n" + "="*70)
    print("BENCHMARK SUMMARY")
    print("="*70)
    
    num_boxes_list, cpp_times_1, python_times_1 = boxes_data
    num_checkpoints_list, cpp_times_2, python_times_2 = checkpoints_data
    
    # Summary for benchmark 1
    avg_speedup_1 = np.mean([p / c for p, c in zip(python_times_1, cpp_times_1)])
    print("\nBenchmark 1 (Varying number of rectangles):")
    print(f"  Average C++ time: {np.mean(cpp_times_1):.4f} seconds")
    print(f"  Average Python time: {np.mean(python_times_1):.4f} seconds")
    print(f"  Average speedup (Python/C++): {avg_speedup_1:.2f}x")
    
    # Summary for benchmark 2
    avg_speedup_2 = np.mean([p / c for p, c in zip(python_times_2, cpp_times_2)])
    print("\nBenchmark 2 (Varying number of measurement points):")
    print(f"  Average C++ time: {np.mean(cpp_times_2):.4f} seconds")
    print(f"  Average Python time: {np.mean(python_times_2):.4f} seconds")
    print(f"  Average speedup (Python/C++): {avg_speedup_2:.2f}x")
    
    print("\n" + "="*70)


def main():
    print("Sky Ratio Calculation - Performance Benchmark")
    print("=" * 70)
    print()
    
    # Run benchmarks
    boxes_data = benchmark_comparison_1()
    checkpoints_data = benchmark_comparison_2()
    
    # Print summary
    print_summary(boxes_data, checkpoints_data)


if __name__ == "__main__":
    main()
