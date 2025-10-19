"""アプリケーションのUIウィジェットの構築と配置を担当します。"""

import tkinter as tk
from tkinter import ttk

class UIBuilder:
    """UIの構築を行うクラス。"""

    def __init__(self, root):
        """UIBuilderオブジェクトを初期化します。

        Args:
            root (tk.Tk): 親となるTkinterルートウィンドウ。
        """
        self.root = root
        self.setup()

    def setup(self):
        """メインウィンドウのUIウィジェットを生成し、配置します。

        このメソッドは、メニューバー、フレーム、ボタン、リストボックス、
        キャンバスなど、アプリケーションの主要なUI要素の生成と
        レイアウトのみを担当します。ウィジェットの具体的な動作（コマンドなど）は
        ここでは設定しません。
        """
        # --- メニューバーの作成 ---
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="ファイル", menu=self.file_menu)
        
        self.export_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="エクスポート", menu=self.export_menu)

        self.format_menu = tk.Menu(self.export_menu, tearoff=0)
        self.export_menu.add_cascade(label="エクスポート形式", menu=self.format_menu)

        # --- メインフレーム ---
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 5))

        # --- UI部品の作成 ---
        self.btn_extract = ttk.Button(top_frame, text="抽出")
        self.btn_extract.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_browse = ttk.Button(top_frame, text="参照...")
        self.btn_browse.pack(side=tk.RIGHT, padx=(5, 0))

        self.entry_filepath = ttk.Entry(top_frame)
        self.entry_filepath.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)

        content_frame = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)

        list_frame = ttk.Frame(content_frame, padding=5)
        content_frame.add(list_frame, weight=1)

        self.list_label = ttk.Label(list_frame, text="検出された領域:")
        self.list_label.pack(anchor=tk.W)
        
        listbox_container = ttk.Frame(list_frame)
        listbox_container.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        self.listbox = tk.Listbox(listbox_container)
        self.listbox_sby = ttk.Scrollbar(listbox_container, orient=tk.VERTICAL)
        self.listbox.configure(yscrollcommand=self.listbox_sby.set)
        self.listbox_sby.config(command=self.listbox.yview)
        
        self.listbox_sby.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        viewer_frame = ttk.Frame(content_frame, padding=5)
        content_frame.add(viewer_frame, weight=4)

        preview_controls_frame = ttk.Frame(viewer_frame)
        preview_controls_frame.pack(fill=tk.X)

        self.viewer_label = ttk.Label(preview_controls_frame, text="PDFプレビュー:")
        self.viewer_label.pack(side=tk.LEFT, anchor=tk.W)

        zoom_frame = ttk.Frame(preview_controls_frame)
        zoom_frame.pack(side=tk.LEFT, padx=20)

        self.zoom_out_btn = ttk.Button(zoom_frame, text="-", width=2)
        self.zoom_out_btn.pack(side=tk.LEFT, padx=5)
        self.scale_label = ttk.Label(zoom_frame, text="100%", width=5, anchor=tk.CENTER)
        self.scale_label.pack(side=tk.LEFT)
        self.zoom_in_btn = ttk.Button(zoom_frame, text="+", width=2)
        self.zoom_in_btn.pack(side=tk.LEFT, padx=5)

        canvas_container = ttk.Frame(viewer_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        self.canvas = tk.Canvas(canvas_container, bg="lightgray")
        self.canvas_vsb = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL)
        self.canvas_hsb = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL)
        self.canvas.configure(yscrollcommand=self.canvas_vsb.set, xscrollcommand=self.canvas_hsb.set)
        self.canvas_vsb.config(command=self.canvas.yview)
        self.canvas_hsb.config(command=self.canvas.xview)

        self.canvas_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # ステータスバー
        self.status_bar = ttk.Label(self.root, text="準備完了", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)