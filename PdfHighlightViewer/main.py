"""アプリケーションのメインエントリポイント。

このスクリプトはアプリケーションを初期化し、メインウィンドウを起動します。
"""
import sys
import os

# スクリプトが直接実行された場合に、パッケージのルートディレクトリをパスに追加します。
# これにより、コマンドラインから直接実行した際にも、
# パッケージ内のモジュールを正しくインポートできるようになります。
if __name__ == "__main__" and __package__ is None:
    # このファイルの親ディレクトリの親ディレクトリ（プロジェクトルート）を取得します。
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Pythonの検索パスの先頭にプロジェクトルートを追加します。
    sys.path.insert(0, project_root)
    # パッケージ名を明示的に設定します。
    __package__ = "PdfHighlightViewer"


from .ui.main_window import MainWindow

def run_app():
    """アプリケーションを起動します。
    """
    # MainWindowがtk.Tkを継承しているため、直接インスタンス化して実行します。
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    run_app()