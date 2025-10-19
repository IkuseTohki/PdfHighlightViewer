# PDF Highlight Viewer

PDF ファイルから特定条件のハイライトや文字を抽出し、一覧表示・エクスポートするためのデスクトップアプリケーションです。

---

## 主な機能

- **多彩な抽出条件**

  - 指定した色の**ハイライト**を抽出
  - 指定した色の**文字**を抽出
  - 指定した**キーワード**を抽出
  - 上記の条件を AND で組み合わせた絞り込み抽出

- **インタラクティブなプレビュー**

  - 抽出した箇所をリストで一覧表示
  - リストで選択した箇所を PDF 上でプレビュー
  - プレビュー画面のズームイン/ズームアウト

- **豊富なエクスポート形式**

  - **PNG:** 選択した箇所、またはすべての箇所を画像として保存
  - **PDF:** 選択した箇所、またはすべての箇所を PDF として再出力
  - **Excel:** すべての箇所の画像、ページ番号、テキストを一覧表として出力

## 実行環境

- Python 3.x
- Windows (Tkinter を使用)

## インストールと実行方法

1. **リポジトリをクローンします。**

   ```bash
   git clone https://github.com/IkuseTohki/PdfHighlightViewer.git
   cd PdfHighlightViewer
   ```

2. **仮想環境を作成し、ライブラリをインストールします。**

   ```bash
   # 仮想環境の作成
   python -m venv .venv

   # 仮想環境のアクティベート
   # (Windowsの場合)
   .venv\Scripts\activate
   # (macOS/Linuxの場合)
   # source .venv/bin/activate

   # 必要なライブラリをインストール
   pip install -r requirements.txt
   ```

   `requirements.txt` に記載されているライブラリは以下の通りです。

   - `PyMuPDF`
   - `Pillow`
   - `openpyxl`

3. **アプリケーションを実行します。**
   ```bash
   python -m PdfHighlightViewer
   ```

## 設定方法

アプリケーションの挙動は、ルートディレクトリにある `setting.ini` ファイルで詳細にカスタマイズできます。

```ini
# --- PDF Highlight Viewer 設定ファイル ---

[UI]
# ユーザーインターフェースに関する設定
HighlightBorderWidth = 3  # プレビュー画面の赤枠の太さ
FontSize = 12             # 全体のフォントサイズ

[Extraction]
# 抽出機能に関する設定
ExtractHighlights = True  # ハイライト色での抽出を有効化
ExtractTextColor = True   # 文字色での抽出を有効化
ExtractKeyword = False    # キーワードでの抽出を有効化
Keyword = ""              # 抽出するキーワード

[HighlightColor]
# 抽出対象とする「ハイライトの色」のRGB範囲 (0-255)
Min_R = 200
Max_R = 255
Min_G = 200
Max_G = 255
Min_B = 0
Max_B = 50

[TextColor]
# 抽出対象とする「文字の色」のRGB範囲 (0-255)
Min_R = 0
Max_R = 50
Min_G = 0
Max_G = 50
Min_B = 230
Max_B = 255

[Export]
# エクスポート機能に関する設定
PdfExportMode = one_page  # PDF一括エクスポートのモード ('one_page' or 'merge')
ExcelImageScale = 1.0     # Excelに貼り付ける画像の拡大率
ImageExportBorderWidth = 2 # 画像/Excelエクスポート時の赤枠の太さ
PdfExportBorderWidth = 1.5 # PDFエクスポート時の赤枠の太さ
```

## ライセンス

このプロジェクトは **MIT License** の下で公開されています。
詳細は `LICENSE` ファイルをご覧ください。
