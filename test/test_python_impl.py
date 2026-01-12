"""
Test script to verify Python implementation works correctly
"""
from python_implementation import SceneRaycasterPython, SkyRatioCheckerPython


def test_python_implementation():
    print("Testing pure Python implementation...")
    
    # Create scene with boxes
    scene = SceneRaycasterPython()
    scene.add_box([5.0, 0.0, 5.0], [2.0, 2.0, 4.0], [0.0, 0.0, 0.0])
    scene.add_box([-5.0, 0.0, 5.0], [2.0, 2.0, 4.0], [0.0, 0.0, 0.0])
    scene.build()
    
    # Create checker
    checker = SkyRatioCheckerPython()
    checker.set_scene(scene)
    checker.ray_resolution = 10.0
    checker.checkpoints = [
        [0.0, 0.0, 1.5],
        [3.0, 0.0, 1.5],
    ]
    
    # Calculate sky ratios
    sky_ratios = checker.check()
    
    print(f"Number of checkpoints: {len(checker.checkpoints)}")
    print(f"Number of results: {len(sky_ratios)}")
    
    for i, (checkpoint, ratio) in enumerate(zip(checker.checkpoints, sky_ratios)):
        print(f"Checkpoint {i + 1} {checkpoint}: {ratio * 100:.2f}%")
    
    assert len(sky_ratios) == 2, "Should have 2 results"
    assert all(0.0 <= r <= 1.0 for r in sky_ratios), "Sky ratios should be between 0 and 1"
    
    print("✓ Python implementation test passed!")


if __name__ == "__main__":
    test_python_implementation()
