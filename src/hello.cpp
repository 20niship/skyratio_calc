#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

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
    m.doc() = "天空率計算プロジェクトのサンプルモジュール";
    
    m.def("add", &add, "2つの整数を加算する");
    m.def("greet", &greet, "名前から挨拶文字列を生成する");
}
