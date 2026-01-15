#pragma once

#include "scene_raycaster.hpp"
#include <tuple>
#include <vector>

class SkyRatioChecker {
private:
  std::vector<std::tuple<Vec3, Vec3>> generate_rays_from_checkpoint(const Vec3& checkpoint);

public:
  std::vector<Vec3> checkpoints;
  float ray_resolution = 1.0f;
  bool use_safe_side   = false; // 安全側評価（内接近似）を使うかどうか

  void set_scene(SceneRaycaster scene);
  std::vector<float> check(SceneRaycaster *raycaster);
};
