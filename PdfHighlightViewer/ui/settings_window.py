import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

class SettingsWindow(tk.Toplevel):
    """設定ウィンドウを表示、管理するクラス。"""
    def __init__(self, parent, settings):
        """SettingsWindowオブジェクトを初期化します。

        Args:
            parent (tk.Widget): 親ウィジェット (MainWindowインスタンス)。
            settings (Settings): アプリケーションの設定オブジェクト。
        """
        super().__init__(parent)
        self.parent = parent
        self.settings = settings
        self.title("抽出条件設定")
        # ウィンドウサイズを広げる
        self.geometry("520x360") 
        self.transient(parent)
        self.grab_set()

        # ウィンドウが閉じられたときのイベントを捕捉
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- 変数定義 ---
        self.extract_highlights_var = tk.BooleanVar(value=self.settings.extract_highlights)
        self.extract_text_color_var = tk.BooleanVar(value=self.settings.extract_text_color)
        self.extract_keyword_var = tk.BooleanVar(value=self.settings.extract_keyword)
        self.extraction_keyword_var = tk.StringVar(value=self.settings.extraction_keyword)

        self.h_min_r, self.h_min_g, self.h_min_b = [tk.StringVar(value=v) for v in self.settings.highlight_color_min]
        self.h_max_r, self.h_max_g, self.h_max_b = [tk.StringVar(value=v) for v in self.settings.highlight_color_max]

        self.t_min_r, self.t_min_g, self.t_min_b = [tk.StringVar(value=v) for v in self.settings.text_color_min]
        self.t_max_r, self.t_max_g, self.t_max_b = [tk.StringVar(value=v) for v in self.settings.text_color_max]

        self.setup_ui()
        self.toggle_keyword_entry()
        self.toggle_color_entries()

    def setup_ui(self):
        """設定ウィンドウのUIウィジェットを生成し、配置します。"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 抽出対象の選択
        target_frame = ttk.LabelFrame(main_frame, text="抽出条件")
        target_frame.pack(pady=5, padx=5, fill=tk.X)

        self.highlight_check = ttk.Checkbutton(
            target_frame, text="ハイライト", variable=self.extract_highlights_var, command=self.toggle_color_entries)
        self.highlight_check.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.highlight_color_frame = self._create_color_entry_frame(target_frame,
                                                                    (self.h_min_r, self.h_min_g, self.h_min_b),
                                                                    (self.h_max_r, self.h_max_g, self.h_max_b))
        self.highlight_color_frame.grid(row=0, column=1, padx=10, pady=5)

        self.color_check = ttk.Checkbutton(
            target_frame, text="文字色", variable=self.extract_text_color_var, command=self.toggle_color_entries)
        self.color_check.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.text_color_frame = self._create_color_entry_frame(target_frame,
                                                               (self.t_min_r, self.t_min_g, self.t_min_b),
                                                               (self.t_max_r, self.t_max_g, self.t_max_b))
        self.text_color_frame.grid(row=1, column=1, padx=10, pady=5)

        keyword_frame = ttk.Frame(target_frame)
        keyword_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

        self.keyword_check = ttk.Checkbutton(
            keyword_frame, text="キーワード:", variable=self.extract_keyword_var, command=self.toggle_keyword_entry)
        self.keyword_check.pack(side=tk.LEFT)

        self.keyword_entry = ttk.Entry(keyword_frame, textvariable=self.extraction_keyword_var)
        self.keyword_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # ボタン
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10, anchor="e")

        self.ok_button = ttk.Button(button_frame, text="OK", command=self.save_settings)
        self.ok_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(button_frame, text="キャンセル", command=self.on_close)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def _create_color_entry_frame(self, parent, min_vars, max_vars):
        """色設定のUI部品を生成するヘルパーメソッド。"""
        frame = ttk.Frame(parent)
        
        ttk.Label(frame, text="R").grid(row=0, column=1, padx=2, pady=(0,2))
        ttk.Label(frame, text="G").grid(row=0, column=2, padx=2, pady=(0,2))
        ttk.Label(frame, text="B").grid(row=0, column=3, padx=2, pady=(0,2))

        ttk.Label(frame, text="Min:").grid(row=1, column=0, padx=2)
        ttk.Entry(frame, textvariable=min_vars[0], width=4).grid(row=1, column=1, padx=2)
        ttk.Entry(frame, textvariable=min_vars[1], width=4).grid(row=1, column=2, padx=2)
        ttk.Entry(frame, textvariable=min_vars[2], width=4).grid(row=1, column=3, padx=2)
        min_btn = ttk.Button(frame, text="色選択", width=8, command=lambda: self._pick_color(min_vars))
        min_btn.grid(row=1, column=4, padx=5)
        min_preview = tk.Label(frame, text=" ", bg="#ffffff", relief="sunken", width=2)
        min_preview.grid(row=1, column=5, padx=(0, 5))

        ttk.Label(frame, text="Max:").grid(row=2, column=0, padx=2)
        ttk.Entry(frame, textvariable=max_vars[0], width=4).grid(row=2, column=1, padx=2)
        ttk.Entry(frame, textvariable=max_vars[1], width=4).grid(row=2, column=2, padx=2)
        ttk.Entry(frame, textvariable=max_vars[2], width=4).grid(row=2, column=3, padx=2)
        max_btn = ttk.Button(frame, text="色選択", width=8, command=lambda: self._pick_color(max_vars))
        max_btn.grid(row=2, column=4, padx=5)
        max_preview = tk.Label(frame, text=" ", bg="#ffffff", relief="sunken", width=2)
        max_preview.grid(row=2, column=5, padx=(0, 5))
        
        self._add_color_trace(min_vars, min_preview)
        self._add_color_trace(max_vars, max_preview)
        
        return frame

    def _add_color_trace(self, rgb_vars, color_label):
        """入力値の変更を監視し、色プレビューを更新するトレースを追加する。"""
        def update_color_preview(*args):
            try:
                r, g, b = int(rgb_vars[0].get()), int(rgb_vars[1].get()), int(rgb_vars[2].get())
                r, g, b = max(0, min(r, 255)), max(0, min(g, 255)), max(0, min(b, 255))
                hex_color = f'#{r:02x}{g:02x}{b:02x}'
                color_label.config(bg=hex_color)
            except (ValueError, tk.TclError):
                color_label.config(bg="#ffffff")

        for var in rgb_vars:
            var.trace_add("write", update_color_preview)
        
        self.after(100, update_color_preview)

    def _pick_color(self, rgb_vars):
        """カラーピッカーを開き、選択した色をStringVarに設定する。"""
        try:
            initial_color = (int(rgb_vars[0].get()), int(rgb_vars[1].get()), int(rgb_vars[2].get()))
            initial_hex = f'#{initial_color[0]:02x}{initial_color[1]:02x}{initial_color[2]:02x}'
        except (ValueError, tk.TclError):
            initial_hex = "#ffffff"

        color = colorchooser.askcolor(color=initial_hex, title="色の選択")
        if color and color[0]:
            r, g, b = color[0]
            rgb_vars[0].set(str(int(r)))
            rgb_vars[1].set(str(int(g)))
            rgb_vars[2].set(str(int(b)))

    def toggle_keyword_entry(self):
        """「キーワード」チェックボックスの状態に応じて入力欄の有効/無効を切り替えます。"""
        state = tk.NORMAL if self.extract_keyword_var.get() else tk.DISABLED
        self.keyword_entry.config(state=state)

    def toggle_color_entries(self):
        """色関連チェックボックスの状態に応じて入力欄の有効/無効を切り替えます。"""
        state = tk.NORMAL if self.extract_highlights_var.get() else tk.DISABLED
        for child in self.highlight_color_frame.winfo_children():
            child.configure(state=state)
        
        state = tk.NORMAL if self.extract_text_color_var.get() else tk.DISABLED
        for child in self.text_color_frame.winfo_children():
            child.configure(state=state)

    def save_settings(self):
        """UIの現在の状態をSettingsオブジェクトに保存し、ファイルを更新します。"""
        try:
            self.settings.extract_highlights = self.extract_highlights_var.get()
            self.settings.extract_text_color = self.extract_text_color_var.get()
            self.settings.extract_keyword = self.extract_keyword_var.get()
            self.settings.extraction_keyword = self.extraction_keyword_var.get()

            self.settings.highlight_color_min = (int(self.h_min_r.get()), int(self.h_min_g.get()), int(self.h_min_b.get()))
            self.settings.highlight_color_max = (int(self.h_max_r.get()), int(self.h_max_g.get()), int(self.h_max_b.get()))
            self.settings.text_color_min = (int(self.t_min_r.get()), int(self.t_min_g.get()), int(self.t_min_b.get()))
            self.settings.text_color_max = (int(self.t_max_r.get()), int(self.t_max_g.get()), int(self.t_max_b.get()))

            self.settings.save()
            self.on_close()
        except ValueError:
            messagebox.showerror("入力エラー", "RGB値は0から255の整数で入力してください。")
        except Exception as e:
            messagebox.showerror("保存エラー", f"設定の保存中にエラーが発生しました:\n{e}")

    def on_close(self):
        """ウィンドウが閉じる際の処理を定義します。

        親ウィンドウ（MainWindow）の抽出ボタンの状態を更新してから、
        このウィンドウを破棄します。
        """
        # 親ウィンドウ (MainWindow) に状態の更新を通知
        if hasattr(self.parent, 'update_extract_button_state'):
            self.parent.update_extract_button_state()
        self.destroy()