"""
天空率計算プロジェクト - 型スタブファイル

このファイルはnanobindによってエクスポートされたC++関数の型情報を提供します。
"""

from typing import List


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
    
    use_safe_side: bool
    """安全側評価（内接近似）を使うかどうか。デフォルトはFalse（外接近似）"""
    
    
    def check(self, scene:SceneRaycaster) -> List[float]:
        """
        各測定点の天空率を計算
        
        Returns:
            各測定点の天空率（0.0〜1.0）のリスト
        """
        ...
