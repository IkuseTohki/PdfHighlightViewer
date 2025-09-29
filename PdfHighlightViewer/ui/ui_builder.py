"""アプリケーションのUIウィジェットの構築と配置を担当します。"""

import tkinter as tk
from tkinter import ttk

from export.formats import ExportFormat

class UIBuilder:
    """UIの構築を行うクラス。"""

    def __init__(self, root, controller):
        """UIBuilderを初期化します。

        Args:
            root (tk.Tk): Tkinterのルートウィンドウ。
            controller: UIイベントを処理するコントローラーオブジェクト（通常はMainWindow）。
        """
        self.root = root
        self.controller = controller

    def setup(self):
        """GUIウィジェットの初期化と配置を行います。"""
        # --- メニューバーの作成 ---
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(label="PDFを開く...", command=self.controller.open_pdf_file)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.root.quit)

        export_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="エクスポート", menu=export_menu)

        format_menu = tk.Menu(export_menu, tearoff=0)
        export_menu.add_cascade(label="エクスポート形式", menu=format_menu)
        format_menu.add_radiobutton(label="画像 (PNG)", variable=self.controller.export_format, value=ExportFormat.PNG.value)
        format_menu.add_radiobutton(label="PDF", variable=self.controller.export_format, value=ExportFormat.PDF.value)
        format_menu.add_radiobutton(label="Excel", variable=self.controller.export_format, value=ExportFormat.EXCEL.value)

        export_menu.add_separator()
        export_menu.add_command(label="選択中のハイライトをエクスポート...", command=self.controller.export_selected_highlight)
        export_menu.add_command(label="すべてのハイライトをエクスポート...", command=self.controller.export_all_highlights)

        # --- メインフレーム ---
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 5))

        self.btn_open = ttk.Button(top_frame, text="PDFを開く", command=self.controller.open_pdf_file)
        self.btn_open.pack(side=tk.LEFT)

        self.lbl_filepath = ttk.Label(top_frame, text="PDFファイルが選択されていません", anchor=tk.W)
        self.lbl_filepath.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        content_frame = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # --- 左ペイン (検出リスト) ---
        list_frame = ttk.Frame(content_frame, padding=5)
        content_frame.add(list_frame, weight=1)

        self.list_label = ttk.Label(list_frame, text="検出された領域:")
        self.list_label.pack(anchor=tk.W)
        
        listbox_container = ttk.Frame(list_frame)
        listbox_container.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        self.listbox = tk.Listbox(listbox_container)
        self.listbox_sby = ttk.Scrollbar(listbox_container, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.listbox_sby.set)
        self.listbox.bind("<<ListboxSelect>>", self.controller.on_list_select)
        
        self.listbox_sby.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- 右ペイン (PDFビューア) ---
        viewer_frame = ttk.Frame(content_frame, padding=5)
        content_frame.add(viewer_frame, weight=4)

        preview_controls_frame = ttk.Frame(viewer_frame)
        preview_controls_frame.pack(fill=tk.X)

        self.viewer_label = ttk.Label(preview_controls_frame, text="PDFプレビュー:")
        self.viewer_label.pack(side=tk.LEFT, anchor=tk.W)

        zoom_frame = ttk.Frame(preview_controls_frame)
        zoom_frame.pack(side=tk.LEFT, padx=20)

        self.zoom_out_btn = ttk.Button(zoom_frame, text="-", command=self.controller.zoom_out, width=2)
        self.zoom_out_btn.pack(side=tk.LEFT, padx=5)
        self.scale_label = ttk.Label(zoom_frame, text=f"{self.controller.scale*100:.0f}%")
        self.scale_label.pack(side=tk.LEFT)
        self.zoom_in_btn = ttk.Button(zoom_frame, text="+", command=self.controller.zoom_in, width=2)
        self.zoom_in_btn.pack(side=tk.LEFT, padx=5)

        canvas_container = ttk.Frame(viewer_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        self.canvas = tk.Canvas(canvas_container, bg="lightgray")
        self.canvas_vsb = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas_hsb = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.canvas_vsb.set, xscrollcommand=self.canvas_hsb.set)

        self.canvas_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
