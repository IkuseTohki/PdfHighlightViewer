import tkinter as tk
from tkinter import ttk

class SettingsWindow(tk.Toplevel):
    """設定画面のウィンドウ。"""

    def __init__(self, parent, controller):
        """SettingsWindowを初期化します。

        Args:
            parent (tk.Widget): 親ウィジェット。
            controller: UIイベントを処理するコントローラーオブジェクト。
        """
        super().__init__(parent)
        self.title("設定")
        self.transient(parent)
        self.grab_set()

        self.controller = controller
        # MainWindowのextraction_modeをコピーして、このウィンドウ内での選択状態を保持
        self.extraction_mode = tk.StringVar(value=self.controller.extraction_mode.get())

        self._setup_widgets()

        self.wait_window(self)

    def _setup_widgets(self):
        """ウィジェットの初期化と配置を行います。"""
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 抽出対象の選択 ---
        mode_frame = ttk.Labelframe(main_frame, text="抽出対象")
        mode_frame.pack(fill=tk.X, pady=5)

        radio_highlight = ttk.Radiobutton(
            mode_frame, text="ハイライト", variable=self.extraction_mode, value="highlight"
        )
        radio_highlight.pack(anchor=tk.W, padx=10, pady=2)

        radio_text = ttk.Radiobutton(
            mode_frame, text="文字色", variable=self.extraction_mode, value="text"
        )
        radio_text.pack(anchor=tk.W, padx=10, pady=2)

        # --- ボタン ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

        ok_button = ttk.Button(button_frame, text="OK", command=self._on_ok)
        ok_button.pack(side=tk.RIGHT, padx=5)

        cancel_button = ttk.Button(button_frame, text="キャンセル", command=self._on_cancel)
        cancel_button.pack(side=tk.RIGHT)

    def _on_ok(self):
        """OKボタンが押されたときの処理。"""
        # MainWindowのextraction_modeに選択結果を反映
        self.controller.extraction_mode.set(self.extraction_mode.get())
        self.destroy()

    def _on_cancel(self):
        """キャンセルボタンが押されたときの処理。"""
        self.destroy()
