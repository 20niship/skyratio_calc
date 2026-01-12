cmake_minimum_required(VERSION 3.15...3.27)
project(sky_ratio_calc)

# Python開発環境を検索
find_package(Python 3.8 COMPONENTS Interpreter Development.Module REQUIRED)

# nanobindの設定
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/src/ext/nanobind)

# Pythonモジュールの作成
nanobind_add_module(sky_ratio_calc src/hello.cpp)

# インストール設定
install(TARGETS sky_ratio_calc LIBRARY DESTINATION .)
