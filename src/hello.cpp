#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/array.h>

#include "scene_raycaster.hpp"
#include "sky_ratio_checker.hpp"

namespace nb = nanobind;

// 簡単な加算関数
int add(int a, int b) {
    return a + b;
}

// 挨拶文字列を返す関数
std::string greet(const std::string& name) {
    return "Hello, " + name + "!";
}

// Pythonモジュールの定義
NB_MODULE(sky_ratio_calc, m) {
    m.doc() = "天空率計算プロジェクト";
    
    m.def("add", &add, "2つの整数を加算する");
    m.def("greet", &greet, "名前から挨拶文字列を生成する");
    
    // HitResult構造体
    nb::class_<HitResult>(m, "HitResult")
        .def(nb::init<>())
        .def_rw("hit", &HitResult::hit)
        .def_rw("position", &HitResult::position)
        .def_rw("distance", &HitResult::distance);
    
    // SceneRaycasterクラス
    nb::class_<SceneRaycaster>(m, "SceneRaycaster")
        .def(nb::init<>())
        .def("clear", &SceneRaycaster::clear, "シーンをクリア")
        .def("add_box", &SceneRaycaster::add_box, 
             nb::arg("pos"), nb::arg("size"), nb::arg("euler"),
             "ボックスを追加")
        .def("add_sphere", &SceneRaycaster::add_sphere,
             nb::arg("center"), nb::arg("radius"),
             "球体を追加")
        .def("add_mesh", &SceneRaycaster::add_mesh,
             nb::arg("vertices"),
             "メッシュを追加")
        .def("build", &SceneRaycaster::build, "BVHを構築")
        .def("raycast", &SceneRaycaster::raycast,
             nb::arg("origins"), nb::arg("directions"),
             "レイキャストを実行");
    
    // SkyRatioCheckerクラス
    nb::class_<SkyRatioChecker>(m, "SkyRatioChecker")
        .def(nb::init<>())
        .def_rw("checkpoints", &SkyRatioChecker::checkpoints, "測定点のリスト")
        .def_rw("ray_resolution", &SkyRatioChecker::ray_resolution, "レイの刻み角度(度)")
        .def("set_scene", &SkyRatioChecker::set_scene,
             nb::arg("scene"),
             "シーンを設定")
        .def("check", &SkyRatioChecker::check, "天空率を計算");
}
