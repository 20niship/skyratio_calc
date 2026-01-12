#pragma once

#include "scene_raycaster.hpp"
#include <vector>
#include <tuple>

class SkyRatioChecker {
private:
    const SceneRaycaster* raycaster = nullptr;
    std::vector<std::tuple<Vec3, Vec3>> generate_rays_from_checkpoint(const Vec3 &checkpoint);

public:
    std::vector<Vec3> checkpoints;
    float ray_resolution = 1.0f;

    void set_scene(const SceneRaycaster &scene);
    std::vector<float> check();
};
