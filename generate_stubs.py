#!/usr/bin/env python3
"""
nanobindでエクスポートされた関数のスタブファイル(.pyi)を生成するスクリプト

使用方法:
    python generate_stubs.py
"""

import sys


def generate_stub_file():
    """スタブファイルを生成"""

    stub_content = '''"""
天空率計算プロジェクト - 型スタブファイル

このファイルはnanobindによってエクスポートされたC++関数の型情報を提供します。
"""

from typing import List

def add(a: int, b: int) -> int:
    """
    2つの整数を加算する
    
    Args:
        a: 1つ目の整数
        b: 2つ目の整数
        
    Returns:
        a + b の結果
    """
    ...

def greet(name: str) -> str:
    """
    名前から挨拶文字列を生成する
    
    Args:
        name: 挨拶する相手の名前
        
    Returns:
        挨拶文字列（"Hello, {name}!"の形式）
    """
    ...

class HitResult:
    """
    レイキャストのヒット結果
    
    Attributes:
        hit: レイがオブジェクトに当たったかどうか
        position: ヒット位置の3D座標 [x, y, z]
        distance: レイの原点からヒット位置までの距離
    """
    
    def __init__(self) -> None:
        """HitResultインスタンスを初期化"""
        ...
    
    hit: bool
    position: List[float]
    distance: float

class SceneRaycaster:
    """
    3Dシーンを構築し、レイキャスト（光線追跡）を実行するクラス
    
    内部ではtiny_bvhライブラリを使用して高速なレイキャストを実現しています。
    """
    
    def __init__(self) -> None:
        """SceneRaycasterインスタンスを初期化"""
        ...
    
    def clear(self) -> None:
        """
        シーンをクリア
        
        追加されたすべてのオブジェクトを削除します。
        """
        ...
    
    def add_box(
        self,
        pos: List[float],
        size: List[float],
        euler: List[float]
    ) -> None:
        """
        ボックスをシーンに追加
        
        Args:
            pos: ボックスの中心位置 [x, y, z]
            size: ボックスのサイズ [width, height, depth]
            euler: オイラー角（回転） [rx, ry, rz] (ラジアン)
        """
        ...
    
    def add_sphere(
        self,
        center: List[float],
        radius: float
    ) -> None:
        """
        球体をシーンに追加
        
        Args:
            center: 球体の中心位置 [x, y, z]
            radius: 球体の半径
        """
        ...
    
    def add_mesh(
        self,
        vertices: List[List[float]]
    ) -> None:
        """
        メッシュをシーンに追加
        
        Args:
            vertices: 頂点のリスト。各頂点は[x, y, z]の形式で、
                     3つの頂点で1つの三角形を構成する
        """
        ...
    
    def build(self) -> None:
        """
        BVH（Bounding Volume Hierarchy）を構築
        
        オブジェクトを追加した後、この関数を呼び出してから
        raycastを実行する必要があります。
        """
        ...
    
    def raycast(
        self,
        origins: List[List[float]],
        directions: List[List[float]]
    ) -> List[HitResult]:
        """
        レイキャストを実行
        
        Args:
            origins: レイの原点のリスト。各原点は[x, y, z]の形式
            directions: レイの方向のリスト。各方向は[x, y, z]の形式（正規化推奨）
            
        Returns:
            各レイのヒット結果のリスト
        """
        ...

class SkyRatioChecker:
    """
    指定した測定点から天空率を計算するクラス
    
    天空率は、測定点から半球状にレイを飛ばし、
    障害物に当たらないレイの割合として計算されます。
    """
    
    def __init__(self) -> None:
        """SkyRatioCheckerインスタンスを初期化"""
        ...
    
    checkpoints: List[List[float]]
    """測定点のリスト。各測定点は[x, y, z]の形式"""
    
    ray_resolution: float
    """レイの角度刻み（度）。デフォルトは1.0度。小さいほど精度が高いが計算時間が増加"""
    
    def set_scene(self, scene: SceneRaycaster) -> None:
        """
        シーンを設定
        
        Args:
            scene: 構築済みのSceneRaycasterオブジェクト
        """
        ...
    
    def check(self) -> List[float]:
        """
        各測定点の天空率を計算
        
        Returns:
            各測定点の天空率（0.0〜1.0）のリスト
        """
        ...
'''
    
    # スタブファイルを書き込み
    stub_path = 'sky_ratio_calc.pyi'
    with open(stub_path, 'w', encoding='utf-8') as f:
        f.write(stub_content)

    print(f"✓ スタブファイルを生成しました: {stub_path}")
    return stub_path


def main():
    """メイン関数"""
    print("天空率計算プロジェクト - スタブファイル生成")
    print("=" * 60)

    try:
        stub_path = generate_stub_file()
        print(f"\n成功: {stub_path} が生成されました")
        print("\nこのファイルにより、IDEでの型チェックとコード補完が有効になります。")
        return 0
    except Exception as e:
        print(f"\nエラー: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
