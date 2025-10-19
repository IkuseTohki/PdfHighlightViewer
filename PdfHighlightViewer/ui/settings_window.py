import tkinter as tk
from tkinter import ttk

class SettingsWindow(tk.Toplevel):
    """設定ウィンドウを表示、管理するクラス。
    """
    def __init__(self, parent, settings):
        """SettingsWindowオブジェクトを初期化します。

        Args:
            parent (tk.Widget): 親ウィジェット (MainWindowインスタンス)。
            settings (Settings): アプリケーションの設定オブジェクト。
        """
        super().__init__(parent)
        self.parent = parent
        self.settings = settings
        self.title("設定")
        self.geometry("350x200")
        self.transient(parent)
        self.grab_set()

        # ウィンドウが閉じられたときのイベントを捕捉
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.extract_highlights_var = tk.BooleanVar(value=self.settings.extract_highlights)
        self.extract_text_color_var = tk.BooleanVar(value=self.settings.extract_text_color)
        self.extract_keyword_var = tk.BooleanVar(value=self.settings.extract_keyword)
        self.extraction_keyword_var = tk.StringVar(value=self.settings.extraction_keyword)

        self.setup_ui()
        self.toggle_keyword_entry()

    def setup_ui(self):
        """設定ウィンドウのUIウィジェットを生成し、配置します。
        """
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 抽出対象の選択
        target_frame = ttk.LabelFrame(main_frame, text="抽出条件 (複数選択可)")
        target_frame.pack(pady=5, padx=5, fill=tk.X)

        self.highlight_check = ttk.Checkbutton(
            target_frame, text="ハイライト", variable=self.extract_highlights_var)
        self.highlight_check.pack(anchor=tk.W, padx=10)

        self.color_check = ttk.Checkbutton(
            target_frame, text="文字色", variable=self.extract_text_color_var)
        self.color_check.pack(anchor=tk.W, padx=10)

        keyword_frame = ttk.Frame(target_frame)
        keyword_frame.pack(anchor=tk.W, padx=10, fill=tk.X)
        
        self.keyword_check = ttk.Checkbutton(
            keyword_frame, text="キーワード:", variable=self.extract_keyword_var, command=self.toggle_keyword_entry)
        self.keyword_check.pack(side=tk.LEFT)

        self.keyword_entry = ttk.Entry(keyword_frame, textvariable=self.extraction_keyword_var)
        self.keyword_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # ボタン
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10, anchor="e")

        self.ok_button = ttk.Button(button_frame, text="OK", command=self.ok_button_action)
        self.ok_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(button_frame, text="キャンセル", command=self.on_close)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def toggle_keyword_entry(self):
        """「キーワード」チェックボックスの状態に応じて入力欄の有効/無効を切り替えます。
        """
        if self.extract_keyword_var.get():
            self.keyword_entry.config(state=tk.NORMAL)
        else:
            self.keyword_entry.config(state=tk.DISABLED)

    def ok_button_action(self):
        """「OK」ボタンが押された際の処理を定義します。

        現在のUIの選択状態を `Settings` オブジェクトに反映し、
        設定ファイルに保存してからウィンドウを閉じます。
        """
        self.settings.extract_highlights = self.extract_highlights_var.get()
        self.settings.extract_text_color = self.extract_text_color_var.get()
        self.settings.extract_keyword = self.extract_keyword_var.get()
        self.settings.extraction_keyword = self.extraction_keyword_var.get()
        self.settings.save_extraction_settings()
        self.on_close()

    def on_close(self):
        """ウィンドウが閉じる際の処理を定義します。

        親ウィンドウ（MainWindow）の抽出ボタンの状態を更新してから、
        このウィンドウを破棄します。
        """
        # 親ウィンドウ (MainWindow) に状態の更新を通知
        if hasattr(self.parent, 'update_extract_button_state'):
            self.parent.update_extract_button_state()
        self.destroy()