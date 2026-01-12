"""
天空率計算の純粋なPython実装
C++実装とのパフォーマンス比較用
"""
import math
from typing import List, Tuple, Optional


class Vec3:
    """3次元ベクトルクラス"""
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return Vec3(self.x / length, self.y / length, self.z / length)
        return Vec3(0, 0, 0)
    
    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]
    
    @staticmethod
    def from_list(lst: List[float]):
        return Vec3(lst[0], lst[1], lst[2])


class Box:
    """軸平行境界ボックス（AABB）"""
    def __init__(self, center: Vec3, size: Vec3):
        self.center = center
        self.size = size
        # 最小・最大境界を計算
        self.min = Vec3(
            center.x - size.x / 2,
            center.y - size.y / 2,
            center.z - size.z / 2
        )
        self.max = Vec3(
            center.x + size.x / 2,
            center.y + size.y / 2,
            center.z + size.z / 2
        )
    
    def intersect_ray(self, origin: Vec3, direction: Vec3) -> Optional[float]:
        """
        スラブ法を使用した光線-ボックス交差判定
        交差する場合は交差点までの距離を返し、しない場合はNoneを返す
        """
        tmin = (self.min.x - origin.x) / direction.x if direction.x != 0 else float('-inf') if origin.x >= self.min.x else float('inf')
        tmax = (self.max.x - origin.x) / direction.x if direction.x != 0 else float('inf') if origin.x <= self.max.x else float('-inf')
        
        if tmin > tmax:
            tmin, tmax = tmax, tmin
        
        tymin = (self.min.y - origin.y) / direction.y if direction.y != 0 else float('-inf') if origin.y >= self.min.y else float('inf')
        tymax = (self.max.y - origin.y) / direction.y if direction.y != 0 else float('inf') if origin.y <= self.max.y else float('-inf')
        
        if tymin > tymax:
            tymin, tymax = tymax, tymin
        
        if (tmin > tymax) or (tymin > tmax):
            return None
        
        tmin = max(tmin, tymin)
        tmax = min(tmax, tymax)
        
        tzmin = (self.min.z - origin.z) / direction.z if direction.z != 0 else float('-inf') if origin.z >= self.min.z else float('inf')
        tzmax = (self.max.z - origin.z) / direction.z if direction.z != 0 else float('inf') if origin.z <= self.max.z else float('-inf')
        
        if tzmin > tzmax:
            tzmin, tzmax = tzmax, tzmin
        
        if (tmin > tzmax) or (tzmin > tmax):
            return None
        
        tmin = max(tmin, tzmin)
        tmax = min(tmax, tzmax)
        
        if tmax < 0:
            return None
        
        return tmin if tmin > 0 else tmax


class SceneRaycasterPython:
    """シーンレイキャストの純粋なPython実装"""
    def __init__(self):
        self.boxes: List[Box] = []
    
    def add_box(self, pos: List[float], size: List[float], euler: List[float] = None):
        """
        シーンにボックスを追加
        
        注意: eulerパラメータはC++版とのAPI互換性のために受け付けますが、
        この簡易Python実装では回転はサポートされていません。
        すべてのボックスは軸平行です。
        
        引数:
            pos: 位置 [x, y, z]
            size: サイズ [幅, 高さ, 奥行き]
            euler: オイラー角（無視される - API互換性のみ）
        
        例外:
            NotImplementedError: 非ゼロのオイラー角が指定された場合
        """
        if euler is not None and any(abs(angle) > 1e-6 for angle in euler):
            raise NotImplementedError(
                "回転（オイラー角）はPython実装ではサポートされていません。"
                "軸平行ボックスのみサポートされています。"
            )
        
        center = Vec3.from_list(pos)
        box_size = Vec3.from_list(size)
        self.boxes.append(Box(center, box_size))
    
    def build(self):
        """加速構造を構築（簡易実装のため何もしない）"""
        pass
    
    def raycast_single(self, origin: Vec3, direction: Vec3) -> Tuple[bool, float]:
        """
        単一の光線を飛ばして(ヒット, 距離)を返す
        """
        min_distance = float('inf')
        hit = False
        
        for box in self.boxes:
            distance = box.intersect_ray(origin, direction)
            if distance is not None and distance < min_distance:
                min_distance = distance
                hit = True
        
        return hit, min_distance if hit else 0.0


class SkyRatioCheckerPython:
    """天空率チェッカーの純粋なPython実装"""
    def __init__(self):
        self.scene: Optional[SceneRaycasterPython] = None
        self.checkpoints: List[List[float]] = []
        self.ray_resolution: float = 1.0
    
    def set_scene(self, scene: SceneRaycasterPython):
        """レイキャストに使用するシーンを設定"""
        self.scene = scene
    
    def generate_rays_from_checkpoint(self, checkpoint: Vec3) -> List[Tuple[Vec3, Vec3]]:
        """測定点から半球状にレイを生成"""
        rays = []
        
        # ray_resolutionの妥当性チェック
        if self.ray_resolution <= 0.0 or self.ray_resolution > 180.0:
            self.ray_resolution = 1.0
        
        resolution_rad = self.ray_resolution * math.pi / 180.0
        
        # Theta: 0度（天頂）から90度（水平）まで
        theta_steps = int(90.0 / self.ray_resolution)
        # Phi: 0度から360度まで
        phi_steps = int(360.0 / self.ray_resolution)
        
        if phi_steps < 1:
            phi_steps = 1
        
        for t in range(theta_steps + 1):
            theta = t * resolution_rad
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)
            
            # 天頂(theta=0)の場合は1本のレイのみ
            current_phi_steps = 1 if t == 0 else phi_steps
            
            for p in range(current_phi_steps):
                phi = p * 2.0 * math.pi / phi_steps
                
                # 球面座標から直交座標への変換
                direction = Vec3(
                    sin_theta * math.cos(phi),
                    sin_theta * math.sin(phi),
                    cos_theta  # Z軸が上方向
                )
                
                rays.append((checkpoint, direction))
        
        return rays
    
    def check(self) -> List[float]:
        """すべての測定点の天空率を計算"""
        if not self.scene:
            return []
        
        results = []
        
        for checkpoint_list in self.checkpoints:
            checkpoint = Vec3.from_list(checkpoint_list)
            rays = self.generate_rays_from_checkpoint(checkpoint)
            
            # レイキャスト実行（一度だけ）
            hit_results = []
            for origin, direction in rays:
                hit, _ = self.scene.raycast_single(origin, direction)
                hit_results.append(hit)
            
            # 積分計算による天空率の計算
            resolution_rad = self.ray_resolution * math.pi / 180.0
            
            theta_steps = int(90.0 / self.ray_resolution)
            phi_steps = int(360.0 / self.ray_resolution)
            if phi_steps < 1:
                phi_steps = 1
            
            # 空が見える部分の投影面積を計算
            sky_area = 0.0
            ray_index = 0
            
            for t in range(theta_steps + 1):
                # レイの角度に対応するセルの範囲を計算
                theta_start = t * resolution_rad
                theta_end = (t + 1) * resolution_rad
                if theta_end > math.pi / 2.0:
                    theta_end = math.pi / 2.0
                
                current_phi_steps = 1 if t == 0 else phi_steps
                
                # このthetaセルの投影面積の重み（phi方向の積分なし）
                theta_area = (math.sin(theta_end) ** 2 - 
                            math.sin(theta_start) ** 2) / 2.0
                
                for p in range(current_phi_steps):
                    if ray_index < len(hit_results) and not hit_results[ray_index]:
                        if t == 0:
                            # 天頂の場合は全周（2π）を代表
                            sky_area += theta_area * 2.0 * math.pi
                        else:
                            # 通常のセルは dPhi の範囲を代表
                            d_phi = 2.0 * math.pi / phi_steps
                            sky_area += theta_area * d_phi
                    ray_index += 1
            
            # 全天の投影面積はπ（半径1の円）
            total_area = math.pi
            sky_ratio = sky_area / total_area if total_area > 0 else 0.0
            results.append(sky_ratio)
        
        return results
