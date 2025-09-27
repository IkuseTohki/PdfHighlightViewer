# PDF Highlight Viewer

## 概要

PDF ファイルに含まれる黄色いハイライト部分を検出し、一覧表示してプレビューできるツールです。
PDF の注釈機能によるハイライトだけでなく、背景色として描画された黄色い矩形も検出対象とします。

## 機能

- PDF ファイルを開く機能
- 黄色い領域（注釈および描画）を自動検出
- 検出した領域をリストとして一覧表示
- リストで選択した項目を、PDF プレビュー上で赤枠表示
- 選択項目への自動ページ遷移およびスクロール
- プレビュー表示の拡大・縮小機能

## ファイル構成

```
.
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── pdf
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   └── renderer.py
│   └── ui
│       ├── __init__.py
│       └── main_window.py
└── README.md
```

## 必要なもの

- Python 3.x
- PyMuPDF
- Pillow

## インストール方法

1. **仮想環境の作成** (推奨)

   ```bash
   python -m venv .venv
   ```

2. **仮想環境のアクティベート**

   - Windows の場合:
     ```bash
     .\.venv\Scripts\activate
     ```
   - macOS / Linux (WSL) の場合:
     ```bash
     source .venv/bin/activate
     ```

3. **必要なライブラリのインストール**
   ```bash
   pip install -r requirements.txt
   ```

## 設定 (Configuration)

プロジェクトのルートディレクトリにある `setting.ini` ファイルを編集することで、検出対象とする色の範囲をカスタマイズできます。

```ini
[ColorRange]
# 抽出したい色のRGB範囲を0-255で指定します
Min_R = 200
Max_R = 255
Min_G = 200
Max_G = 255
Min_B = 0
Max_B = 50
```

- `Min_R`, `Min_G`, `Min_B`: 検出対象とする色の、赤・緑・青のそれぞれの最小値 (0-255)
- `Max_R`, `Max_G`, `Max_B`: 検出対象とする色の、赤・緑・青のそれぞれの最大値 (0-255)

設定を変更した後は、アプリケーションを再起動してください。

## 使い方

以下のコマンドでアプリケーションを起動します。

```bash
python src/main.py
```
