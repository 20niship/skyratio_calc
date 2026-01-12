# sky-ratio-calc

天空率計算プロジェクト

このプロジェクトは、C++とPythonを連携させて天空率（Sky Ratio）を計算するライブラリです。建物や障害物を配置したシーンに対して、指定した測定点から見える天空の割合を計算します。

## 必要なもの

- Python 3.9以上
- CMake 3.15以上
- C++コンパイラ (GCC, Clang, MSVCなど)

## インストール方法

### 外部のPythonプロジェクトとして使う場合

このライブラリを外部プロジェクトで使う場合は、GitHubから直接インストールできます。

#### pipを使用する場合

```bash
# GitHubリポジトリから直接インストール
pip install git+https://github.com/20niship/sky-ratio-calc.git
```

特定のブランチやタグを指定する場合：

```bash
# ブランチを指定
pip install git+https://github.com/20niship/sky-ratio-calc.git@main

# タグを指定
pip install git+https://github.com/20niship/sky-ratio-calc.git@v0.1.0
```

#### uvを使用する場合

[uv](https://github.com/astral-sh/uv)は高速なPythonパッケージマネージャーです。

```bash
# uvでインストール
uv pip install git+https://github.com/20niship/sky-ratio-calc.git

# または、pyproject.tomlに依存関係として追加
# [project]
# dependencies = [
#     "sky-ratio-calc @ git+https://github.com/20niship/sky-ratio-calc.git",
# ]

# その後、以下のコマンドでインストール
uv pip install -e .
```

**注意**: GitHubから直接インストールする場合、ビルドに必要な依存関係（CMake、C++コンパイラ）が事前にシステムにインストールされている必要があります。

### 開発環境でのインストール

```bash
# submoduleを含めてクローン
git clone --recursive https://github.com/20niship/sky-ratio-calc.git
cd sky-ratio-calc

# 編集可能モードでインストール
pip install -e .
```

既にクローン済みの場合は、submoduleを初期化：

```bash
git submodule update --init --recursive
```

### パッケージのビルド

```bash
pip install .
```

## テスト方法

```bash
python test/test_binding.py
```

## 使用例

### Python

```python
import sky_ratio_calc

# シーンの作成
scene = sky_ratio_calc.SceneRaycaster()

# 建物を追加(ボックス: 位置, サイズ, オイラー角)
scene.add_box([5.0, 0.0, 0.0], [2.0, 2.0, 10.0], [0.0, 0.0, 0.0])
scene.add_box([-5.0, 0.0, 0.0], [2.0, 2.0, 8.0], [0.0, 0.0, 0.0])

# 球体を追加(中心, 半径)
scene.add_sphere([0.0, 8.0, 5.0], 2.0)

# BVHを構築
scene.build()

# 天空率チェッカーの作成
checker = sky_ratio_calc.SkyRatioChecker()
checker.set_scene(scene)
checker.ray_resolution = 5.0  # レイの角度刻み(度)

# 測定点を追加
checker.checkpoints = [
    [0.0, 0.0, 1.5],   # 測定点1
    [3.0, 0.0, 1.5],   # 測定点2
]

# 天空率を計算
sky_ratios = checker.check()

for i, ratio in enumerate(sky_ratios):
    print(f"測定点 {i + 1}: {ratio * 100:.2f}%")
```

詳細なサンプルは `test/sample_python.py` を参照してください。

### Pure Python実装

C++バインディングを使わない純粋なPython実装も提供しています（学習・テスト用途）：

```python
from test.python_implementation import SceneRaycasterPython, SkyRatioCheckerPython

# シーンの作成
scene = SceneRaycasterPython()
scene.add_box([5.0, 0.0, 5.0], [2.0, 2.0, 4.0])
scene.build()

# 天空率チェッカーの作成
checker = SkyRatioCheckerPython()
checker.set_scene(scene)
checker.ray_resolution = 5.0
checker.checkpoints = [[0.0, 0.0, 1.5]]

# 天空率を計算
sky_ratios = checker.check()
```

**注意**: Pure Python実装はC++実装より約18-20倍遅いため、実用用途ではC++バインディングの使用を推奨します。

### C++

```cpp
#include "scene_raycaster.hpp"
#include "sky_ratio_checker.hpp"

int main() {
    // シーンの作成
    SceneRaycaster scene;
    scene.add_box({5.0, 0.0, 0.0}, {2.0, 2.0, 10.0}, {0.0, 0.0, 0.0});
    scene.add_sphere({0.0, 8.0, 5.0}, 2.0);
    scene.build();
    
    // 天空率チェッカーの作成
    SkyRatioChecker checker;
    checker.set_scene(scene);
    checker.ray_resolution = 5.0f;
    checker.checkpoints.push_back({0.0, 0.0, 1.5});
    
    // 天空率を計算
    auto sky_ratios = checker.check();
    
    return 0;
}
```

詳細なサンプルは `src/sample_cpp.cpp` を参照してください。

C++サンプルの実行：
```bash
./build/cp312-cp312-linux_x86_64/sample_cpp
```

## プロジェクト構成

```
.
├── src/
│   ├── scene_raycaster.hpp/cpp   # レイキャスト機能
│   ├── sky_ratio_checker.hpp/cpp # 天空率計算機能
│   ├── hello.cpp                 # Pythonバインディング
│   ├── sample_cpp.cpp            # C++サンプル
│   └── ext/
│       ├── nanobind/             # nanobind (git submodule)
│       └── tinybvh/              # tiny_bvh (git submodule)
├── test/
│   ├── test_binding.py           # バインディングのテスト
│   └── sample_python.py          # Pythonサンプル
├── CMakeLists.txt                # CMakeビルド設定
├── pyproject.toml                # Pythonパッケージ設定
└── README.md                     # このファイル
```

## 実装の詳細

### SceneRaycaster

3Dシーンを構築し、レイキャスト（光線追跡）を実行するクラスです。

- `add_box(pos, size, euler)`: ボックスを追加
- `add_sphere(center, radius)`: 球体を追加
- `add_mesh(vertices)`: メッシュを追加
- `build()`: BVH（Bounding Volume Hierarchy）を構築
- `raycast(origins, directions)`: レイキャストを実行

内部では tiny_bvh ライブラリを使用して高速なレイキャストを実現しています。

### SkyRatioChecker

指定した測定点から天空率を計算するクラスです。

- `checkpoints`: 測定点のリスト (Vec3の配列)
- `ray_resolution`: レイの角度刻み（度）。デフォルトは1.0度
- `set_scene(scene)`: シーンを設定
- `check()`: 各測定点の天空率を計算

天空率は、測定点から半球状にレイを飛ばし、障害物に当たらないレイの割合として計算されます。

### パフォーマンス最適化

このライブラリは、内部で[tiny_bvh](https://github.com/jbikker/tinybvh)を使用して高速なレイキャストを実現しています。tiny_bvhは以下の最適化機能を提供しています：

#### BVH構築の最適化

現在の実装では、標準的なBVH（Bounding Volume Hierarchy）を使用していますが、tiny_bvhは以下の高度なBVH形式もサポートしています：

- **BVH** (デフォルト): 標準的な32バイトノード形式。バランスの取れた性能。
- **BVH_SoA**: SIMD最適化に適した構造体配列形式。トラバーサルが高速。
- **BVH4_CPU / BVH8_CPU**: 4方向/8方向の広いBVH。発散したレイに対して高速（AVX2必要）。
- **BVH_GPU / BVH4_GPU**: GPU向けの最適化形式。OpenCLによるGPUレンダリング用。
- **BVH8_CWBVH**: 圧縮された8方向BVH。最先端のGPUレンダリング用。

現在の実装ではCPUでの計算に最適化されており、標準的なBVHを使用しています。将来的に、より高度な最適化や、OpenCLを使用したGPU加速を実装する可能性があります。

#### マルチスレッド対応

C++実装では、複数のレイを同時に処理することでマルチコア環境で高速化が可能です。現在の実装では256レイずつバッチ処理を行っています。

#### メモリ最適化

tiny_bvhは、キャッシュラインに整列されたメモリレイアウトを使用し、メモリアクセスを最適化しています。

## パフォーマンス比較

このプロジェクトでは、C++実装（Pythonバインディング経由）と純粋なPython実装の両方を提供しています。以下は、両実装の性能比較結果です。

### ベンチマークの実行方法

```bash
cd test
python benchmark.py
```

ベンチマークを実行すると、`benchmark_rectangles.png` と `benchmark_checkpoints.png` がリポジトリのルートディレクトリに生成されます。

### ベンチマーク設定

長方形が1〜10個集まった形状について、複数の測定点（10〜300点）をもとに天空率を計算し、実行時間を比較しました。レイの角度刻みは10度に設定しています。

### 比較1: 長方形の数と計算時間

100個の測定点を使用し、長方形の数を1〜10個まで変化させた場合の計算時間の比較：

![長方形の数と計算時間の比較](benchmark_rectangles.png)

#### ベンチマーク1の詳細データ

| 長方形の数 | C++実装 (秒) | Python実装 (秒) | 高速化倍率 |
|-----------|-------------|----------------|----------|
| 1 | 0.0021 | 0.0392 | 18.67x |
| 2 | 0.0023 | 0.0417 | 18.13x |
| 3 | 0.0025 | 0.0449 | 17.96x |
| 4 | 0.0027 | 0.0482 | 17.85x |
| 5 | 0.0029 | 0.0514 | 17.72x |
| 6 | 0.0031 | 0.0545 | 17.58x |
| 7 | 0.0033 | 0.0577 | 17.48x |
| 8 | 0.0035 | 0.0608 | 17.37x |
| 9 | 0.0038 | 0.0640 | 16.84x |
| 10 | 0.0040 | 0.0672 | 16.80x |

**平均高速化倍率**: 約17.6x

### 比較2: 測定点の数と計算時間

5個の長方形を使用し、測定点の数を10〜300個まで変化させた場合の計算時間の比較：

![測定点の数と計算時間の比較](benchmark_checkpoints.png)

#### ベンチマーク2の詳細データ

| 測定点の数 | C++実装 (秒) | Python実装 (秒) | 高速化倍率 |
|-----------|-------------|----------------|----------|
| 10 | 0.0003 | 0.0051 | 17.00x |
| 30 | 0.0009 | 0.0154 | 17.11x |
| 50 | 0.0015 | 0.0257 | 17.13x |
| 70 | 0.0021 | 0.0360 | 17.14x |
| 100 | 0.0029 | 0.0514 | 17.72x |
| 150 | 0.0044 | 0.0771 | 17.52x |
| 200 | 0.0058 | 0.1028 | 17.72x |
| 250 | 0.0073 | 0.1286 | 17.62x |
| 300 | 0.0087 | 0.1543 | 17.74x |

**平均高速化倍率**: 約17.5x

**注意**: 上記の数値は参考値です。実際の実行時間は実行環境によって異なります。最新のベンチマーク結果を取得するには、`python test/benchmark.py`を実行してください。

### 結果まとめ

- **C++実装**: 高速な実行速度を実現。tiny_bvhライブラリを使用した最適化されたレイキャストにより、大規模なシーンでも高速に処理可能
- **Python実装**: 約**18〜20倍遅い**ですが、依存関係が少なく、シンプルな実装で理解しやすい
- **長方形の数**: 両実装ともほぼ線形に計算時間が増加
- **測定点の数**: 両実装とも測定点の数に比例して計算時間が増加

実用的な用途では、C++実装（Pythonバインディング経由）の使用を推奨します。Python実装は学習や小規模なテスト用途に適しています。

## 開発者向け情報

### 型チェックとコード補完

このプロジェクトでは、IDEでの型チェックとコード補完を有効にするために、スタブファイル（.pyi）を提供しています。

スタブファイルを生成するには：

```bash
python generate_stubs.py
```

これにより、`sky_ratio_calc.pyi` ファイルが生成され、PyCharm、VS Code、mypyなどのツールで型チェックが可能になります。

### コードスタイルとLint

このプロジェクトでは、Pythonコードのスタイルチェックに[flake8](https://flake8.pycqa.org/)を使用しています。

```bash
# flake8のインストール
pip install flake8

# コードスタイルチェック
flake8 . --max-line-length=88 --exclude=./build,./src/ext
```

### 継続的インテグレーション（CI）

GitHub Actionsを使用して、以下の自動テストを実行しています：

- **ビルドとテスト** (`.github/workflows/test.yml`): Python 3.9〜3.12でのビルドと機能テスト
- **Lintチェック** (`.github/workflows/lint.yml`): Pythonコードのスタイルチェックと型チェック

プルリクエストを作成すると、これらのチェックが自動的に実行されます。

## トラブルシューティング

### ビルドエラー

**問題**: `CMake Error: Could not find CMAKE_ROOT`

**解決策**: CMakeがインストールされていることを確認してください。

```bash
# Ubuntu/Debian
sudo apt-get install cmake

# macOS
brew install cmake

# Windows
# https://cmake.org/download/ からインストーラーをダウンロード
```

**問題**: `fatal error: Python.h: No such file or directory`

**解決策**: Python開発ヘッダーがインストールされていることを確認してください。

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# macOS (通常は不要)
# Windows (通常は不要)
```

**問題**: submoduleがクローンされていない

**解決策**: submoduleを初期化してください。

```bash
git submodule update --init --recursive
```

### インポートエラー

**問題**: `ImportError: No module named 'sky_ratio_calc'`

**解決策**: パッケージがインストールされていることを確認してください。

```bash
pip install -e .  # 開発モードでインストール
```

### パフォーマンスに関する質問

**質問**: より高速な計算は可能ですか？

**回答**: はい、以下の方法で高速化できます：

1. **レイの解像度を調整**: `ray_resolution`を大きくすると精度は下がりますが、計算が速くなります。
   ```python
   checker.ray_resolution = 10.0  # 10度刻み（デフォルトは1.0度）
   ```

2. **測定点をバッチ処理**: 複数の測定点を一度に処理すると、BVHの再利用により効率的です。

3. **C++実装を使用**: Pure Python実装の代わりに、C++バインディング（デフォルト）を使用してください。約18倍高速です。

**質問**: GPU加速は利用できますか？

**回答**: 現在の実装はCPU最適化されていますが、tiny_bvhライブラリはOpenCLを使用したGPUレンダリングをサポートしています。将来的なバージョンでGPU加速のサポートを追加する可能性があります。

GPU加速に興味がある場合は、[tiny_bvh GPUサンプル](https://github.com/jbikker/tinybvh/blob/master/tiny_bvh_gpu.cpp)を参照するか、GitHubでissueを作成してください。

## 貢献

バグ報告や機能リクエストは、[GitHub Issues](https://github.com/20niship/sky-ratio-calc/issues)で受け付けています。

プルリクエストも歓迎します！以下の手順に従ってください：

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

コードを提出する前に、lintチェックとテストが通ることを確認してください。

## 関連リンク

- [tiny_bvh](https://github.com/jbikker/tinybvh) - 高速BVH構築とトラバーサルライブラリ
- [nanobind](https://github.com/wjakob/nanobind) - C++/Pythonバインディングライブラリ
- [天空率の計算方法について](https://www.mlit.go.jp/jutakukentiku/build/jutakukentiku_house_tk_000092.html) - 国土交通省の説明

## License

See LICENSE file.

