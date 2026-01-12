# sky-ratio-calc

天空率計算プロジェクト - nanobindサンプル

このプロジェクトは、C++とPythonを連携させるためのnanobindを使用したサンプルです。

## 必要なもの

- Python 3.8以上
- CMake 3.15以上
- C++コンパイラ (GCC, Clang, MSVCなど)

## ビルド方法

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

```python
import sky_ratio_calc

# 加算
result = sky_ratio_calc.add(3, 5)
print(f"3 + 5 = {result}")  # 出力: 3 + 5 = 8

# 挨拶
greeting = sky_ratio_calc.greet("World")
print(greeting)  # 出力: Hello, World!
```

## プロジェクト構成

```
.
├── src/
│   ├── hello.cpp           # C++実装とnanobindバインディング
│   └── ext/
│       └── nanobind/       # nanobind (git submodule)
├── test/
│   └── test_binding.py     # バインディングのテスト
├── CMakeLists.txt          # CMakeビルド設定
├── pyproject.toml          # Pythonパッケージ設定
└── README.md               # このファイル
```

## License

See LICENSE file.
