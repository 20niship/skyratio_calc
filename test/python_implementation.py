"""
Pure Python implementation of sky ratio calculation
This is for performance comparison with the C++ implementation
"""
import math
from typing import List, Tuple, Optional


class Vec3:
    """3D vector class"""
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
    """Axis-aligned bounding box"""
    def __init__(self, center: Vec3, size: Vec3):
        self.center = center
        self.size = size
        # Calculate min and max bounds
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
        Ray-box intersection test using slab method
        Returns distance to intersection point if hit, None otherwise
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
    """Pure Python implementation of scene raycasting"""
    def __init__(self):
        self.boxes: List[Box] = []
    
    def add_box(self, pos: List[float], size: List[float], euler: List[float] = None):
        """
        Add a box to the scene
        
        Note: euler parameter is accepted for API compatibility with C++ version,
        but rotation is not supported in this simplified Python implementation.
        All boxes are axis-aligned.
        """
        center = Vec3.from_list(pos)
        box_size = Vec3.from_list(size)
        self.boxes.append(Box(center, box_size))
    
    def build(self):
        """Build acceleration structure (no-op for simple implementation)"""
        pass
    
    def raycast_single(self, origin: Vec3, direction: Vec3) -> Tuple[bool, float]:
        """
        Cast a single ray and return (hit, distance)
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
    """Pure Python implementation of sky ratio checker"""
    def __init__(self):
        self.scene: Optional[SceneRaycasterPython] = None
        self.checkpoints: List[List[float]] = []
        self.ray_resolution: float = 1.0
    
    def set_scene(self, scene: SceneRaycasterPython):
        """Set the scene to use for raycasting"""
        self.scene = scene
    
    def generate_rays_from_checkpoint(self, checkpoint: Vec3) -> List[Tuple[Vec3, Vec3]]:
        """Generate hemisphere rays from a checkpoint"""
        rays = []
        
        # Validate ray_resolution
        if self.ray_resolution <= 0.0 or self.ray_resolution > 180.0:
            self.ray_resolution = 1.0
        
        resolution_rad = self.ray_resolution * math.pi / 180.0
        
        # Theta: 0 degrees (zenith) to 90 degrees (horizontal)
        theta_steps = int(90.0 / self.ray_resolution)
        # Phi: 0 degrees to 360 degrees
        phi_steps = int(360.0 / self.ray_resolution)
        
        if phi_steps < 1:
            phi_steps = 1
        
        for t in range(theta_steps + 1):
            theta = t * resolution_rad
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)
            
            # At zenith (theta=0), only one ray
            current_phi_steps = 1 if t == 0 else phi_steps
            
            for p in range(current_phi_steps):
                phi = p * 2.0 * math.pi / phi_steps
                
                # Spherical to Cartesian coordinates
                direction = Vec3(
                    sin_theta * math.cos(phi),
                    sin_theta * math.sin(phi),
                    cos_theta  # Z-axis is up
                )
                
                rays.append((checkpoint, direction))
        
        return rays
    
    def check(self) -> List[float]:
        """Calculate sky ratio for all checkpoints"""
        if not self.scene:
            return []
        
        results = []
        
        for checkpoint_list in self.checkpoints:
            checkpoint = Vec3.from_list(checkpoint_list)
            rays = self.generate_rays_from_checkpoint(checkpoint)
            
            # Count rays that don't hit anything (can see the sky)
            sky_visible_count = 0
            for origin, direction in rays:
                hit, _ = self.scene.raycast_single(origin, direction)
                if not hit:
                    sky_visible_count += 1
            
            # Calculate sky ratio
            sky_ratio = sky_visible_count / len(rays) if rays else 0.0
            results.append(sky_ratio)
        
        return results
