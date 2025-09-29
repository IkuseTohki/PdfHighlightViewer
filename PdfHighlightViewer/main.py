"""アプリケーションのメインエントリポイント。

このスクリプトはアプリケーションを初期化し、メインウィンドウを起動します。
"""

import tkinter as tk
from ui.main_window import MainWindow

def run_app():
    # Tkinterのルートウィンドウを作成
    root = tk.Tk()
    # メインウィンドウのクラスをインスタンス化
    app = MainWindow(root)
    # Tkinterのメインループを開始
    root.mainloop()

if __name__ == "__main__":
    run_app()
