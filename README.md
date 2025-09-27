# PDF Highlight Viewer

## 概要

PDFファイルに含まれる黄色いハイライト部分を検出し、一覧表示してプレビューできるツールです。
PDFの注釈機能によるハイライトだけでなく、背景色として描画された黄色い矩形も検出対象とします。

## 機能

- PDFファイルを開く機能
- 黄色い領域（注釈および描画）を自動検出
- 検出した領域をリストとして一覧表示
- リストで選択した項目を、PDFプレビュー上で赤枠表示
- 選択項目への自動ページ遷移およびスクロール

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

1.  **仮想環境の作成** (推奨)
    ```bash
    python -m venv .venv
    ```

2.  **仮想環境のアクティベート**
    - Windowsの場合:
      ```bash
      .\.venv\Scripts\activate
      ```
    - macOS / Linux (WSL) の場合:
      ```bash
      source .venv/bin/activate
      ```

3.  **必要なライブラリのインストール**
    ```bash
    pip install PyMuPDF Pillow
    ```

## 使い方

以下のコマンドでアプリケーションを起動します。

```bash
python src/main.py
```
