"""
C++バインディングのテスト
"""
import sky_ratio_calc


def test_add():
    """add関数のテスト"""
    result = sky_ratio_calc.add(3, 5)
    assert result == 8, f"Expected 8, got {result}"
    print(f"✓ add(3, 5) = {result}")


def test_greet():
    """greet関数のテスト"""
    result = sky_ratio_calc.greet("World")
    assert result == "Hello, World!", f"Expected 'Hello, World!', got '{result}'"
    print(f"✓ greet('World') = '{result}'")


if __name__ == "__main__":
    test_add()
    test_greet()
    print("\nすべてのテストが成功しました！")
