"""アプリケーションのメインエントリポイント。

このスクリプトはアプリケーションを初期化し、メインウィンドウを起動します。
"""

from .ui.main_window import MainWindow

def run_app():
    """アプリケーションを起動します。
    """
    # MainWindowがtk.Tkを継承しているため、直接インスタンス化して実行します。
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    run_app()
