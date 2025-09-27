import tkinter as tk
from ui.main_window import MainWindow

if __name__ == "__main__":
    """
    アプリケーションのエントリポイント。
    """
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
