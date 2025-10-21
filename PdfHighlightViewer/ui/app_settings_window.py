import tkinter as tk
from tkinter import ttk, messagebox

from ..config.settings import Settings
from ..export.formats import ExportFormat, PdfExportMode

class AppSettingsWindow(tk.Toplevel):
    """アプリケーション全体の設定ウィンドウを表示、管理するクラス。"""
    def __init__(self, parent, settings):
        """AppSettingsWindowオブジェクトを初期化します。

        Args:
            parent (tk.Widget): 親ウィジェット (MainWindowインスタンス)。
            settings (Settings): アプリケーションの設定オブジェクト。
        """
        super().__init__(parent)
        self.parent = parent
        self.settings = settings
        self.title("アプリケーション設定")
        self.geometry("450x500") # 高さをさらに増やす
        self.transient(parent)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- 変数定義 ---
        # UI設定
        self.highlight_border_width_var = tk.IntVar(value=self.settings.highlight_border_width)
        self.font_size_var = tk.IntVar(value=self.settings.font_size)

        # エクスポート設定
        self.pdf_export_mode_var = tk.StringVar(value=self.settings.pdf_export_mode)
        self.excel_image_scale_var = tk.DoubleVar(value=self.settings.excel_image_scale)
        self.image_export_border_width_var = tk.IntVar(value=self.settings.image_export_border_width)
        self.pdf_export_border_width_var = tk.DoubleVar(value=self.settings.pdf_export_border_width)

        self.setup_ui()

    def setup_ui(self):
        """設定ウィンドウのUIウィジェットを生成し、配置します。"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- UI設定フレーム ---
        ui_frame = ttk.LabelFrame(main_frame, text="UI設定")
        ui_frame.pack(pady=10, padx=5, fill=tk.X)

        ttk.Label(ui_frame, text="プレビュー枠線太さ:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(ui_frame, from_=1, to_=10, textvariable=self.highlight_border_width_var, width=5).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(ui_frame, text="フォントサイズ:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(ui_frame, from_=8, to_=24, textvariable=self.font_size_var, width=5).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # --- エクスポート設定フレーム ---
        export_frame = ttk.LabelFrame(main_frame, text="エクスポート設定")
        export_frame.pack(pady=10, padx=5, fill=tk.X)

        # --- PDFエクスポート設定 ---
        pdf_export_frame = ttk.LabelFrame(export_frame, text="PDFエクスポート")
        pdf_export_frame.pack(pady=5, padx=5, fill=tk.X)

        ttk.Label(pdf_export_frame, text="PDF一括エクスポートモード:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        mode_frame = ttk.Frame(pdf_export_frame)
        mode_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="1ページずつ", variable=self.pdf_export_mode_var, value=PdfExportMode.ONE_PAGE.value).pack(side=tk.LEFT, pady=2)
        ttk.Radiobutton(mode_frame, text="ページ統合", variable=self.pdf_export_mode_var, value=PdfExportMode.MERGE.value).pack(side=tk.LEFT, padx=10, pady=2)

        ttk.Label(pdf_export_frame, text="PDFエクスポート枠線太さ:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(pdf_export_frame, from_=0.5, to_=5.0, increment=0.1, textvariable=self.pdf_export_border_width_var, width=5, format="%.1f").grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # --- 画像/Excelエクスポート設定 ---
        img_excel_export_frame = ttk.LabelFrame(export_frame, text="画像/Excelエクスポート")
        img_excel_export_frame.pack(pady=5, padx=5, fill=tk.X)

        ttk.Label(img_excel_export_frame, text="Excel画像拡大率:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(img_excel_export_frame, from_=0.5, to_=5.0, increment=0.1, textvariable=self.excel_image_scale_var, width=5, format="%.1f").grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(img_excel_export_frame, text="画像/Excel枠線太さ:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(img_excel_export_frame, from_=1, to_=10, textvariable=self.image_export_border_width_var, width=5).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # --- ボタン ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15, anchor="e")

        self.ok_button = ttk.Button(button_frame, text="OK", command=self.save_settings)
        self.ok_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(button_frame, text="キャンセル", command=self.on_close)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def save_settings(self):
        """UIの現在の状態をSettingsオブジェクトに保存し、ファイルを更新します。"""
        try:
            # UI設定
            self.settings.highlight_border_width = self.highlight_border_width_var.get()
            self.settings.font_size = self.font_size_var.get()

            # エクスポート設定
            self.settings.pdf_export_mode = self.pdf_export_mode_var.get()
            self.settings.excel_image_scale = self.excel_image_scale_var.get()
            self.settings.image_export_border_width = self.image_export_border_width_var.get()
            self.settings.pdf_export_border_width = self.pdf_export_border_width_var.get()

            self.settings.save()
            self.on_close()
        except Exception as e:
            messagebox.showerror("保存エラー", f"設定の保存中にエラーが発生しました:\n{e}")

    def on_close(self):
        """ウィンドウが閉じる際の処理を定義します。"""
        self.destroy()
