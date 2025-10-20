import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

@dataclass
class UIWidgets:
    """アプリケーションのUIウィジェットを保持するデータクラス。"""
    # メニュー
    menubar: tk.Menu = None
    file_menu: tk.Menu = None
    export_menu: tk.Menu = None
    format_menu: tk.Menu = None
    # 上部パネル
    btn_extract: ttk.Button = None
    btn_browse: ttk.Button = None
    entry_filepath: ttk.Entry = None
    # リストボックスパネル
    list_label: ttk.Label = None
    listbox: tk.Listbox = None
    listbox_sby: ttk.Scrollbar = None
    # ビューアパネル
    viewer_label: ttk.Label = None
    zoom_out_btn: ttk.Button = None
    scale_label: ttk.Label = None
    zoom_in_btn: ttk.Button = None
    canvas: tk.Canvas = None
    canvas_vsb: ttk.Scrollbar = None
    canvas_hsb: ttk.Scrollbar = None
    # ステータスバー
    status_bar: ttk.Label = None


class UIBuilder:
    """UIの構築を行うクラス。"""

    def __init__(self, root):
        """UIBuilderオブジェクトを初期化します。

        Args:
            root (tk.Tk): 親となるTkinterルートウィンドウ。
        """
        self.root = root
        self.widgets = UIWidgets()
        self.setup()

    def setup(self):
        """メインウィンドウのUIを構築するための各コンポーネント生成メソッドを呼び出します。"""
        self._create_menubar()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._create_top_panel(main_frame)
        self._create_content_panels(main_frame)
        self._create_statusbar()

    def _create_menubar(self):
        """メニューバーを生成し、ルートウィンドウに配置します。"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        
        export_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="エクスポート", menu=export_menu)

        format_menu = tk.Menu(export_menu, tearoff=0)
        export_menu.add_cascade(label="エクスポート形式", menu=format_menu)

        self.widgets.menubar = menubar
        self.widgets.file_menu = file_menu
        self.widgets.export_menu = export_menu
        self.widgets.format_menu = format_menu

    def _create_top_panel(self, parent):
        """ファイル選択に関連する上部パネルを生成します。

        Args:
            parent (tk.Widget): このパネルを配置する親ウィジェット。
        """
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, pady=(0, 5))

        btn_extract = ttk.Button(top_frame, text="抽出")
        btn_extract.pack(side=tk.LEFT, padx=(0, 5))

        btn_browse = ttk.Button(top_frame, text="参照...")
        btn_browse.pack(side=tk.RIGHT, padx=(5, 0))

        entry_filepath = ttk.Entry(top_frame)
        entry_filepath.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)

        self.widgets.btn_extract = btn_extract
        self.widgets.btn_browse = btn_browse
        self.widgets.entry_filepath = entry_filepath

    def _create_content_panels(self, parent):
        """リストボックスとPDFビューアを含むメインコンテンツパネルを生成します。

        Args:
            parent (tk.Widget): このパネルを配置する親ウィジェット。
        """
        content_frame = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)

        self._create_listbox_panel(content_frame)
        self._create_viewer_panel(content_frame)

    def _create_listbox_panel(self, parent):
        """検出された領域を表示するリストボックスパネルを生成します。

        Args:
            parent (tk.PanedWindow): このパネルを追加する親のPanedWindow。
        """
        list_frame = ttk.Frame(parent, padding=5)
        parent.add(list_frame, weight=1)

        list_label = ttk.Label(list_frame, text="検出された領域:")
        list_label.pack(anchor=tk.W)
        
        listbox_container = ttk.Frame(list_frame)
        listbox_container.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        listbox = tk.Listbox(listbox_container)
        listbox_sby = ttk.Scrollbar(listbox_container, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=listbox_sby.set)
        
        listbox_sby.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.widgets.list_label = list_label
        self.widgets.listbox = listbox
        self.widgets.listbox_sby = listbox_sby

    def _create_viewer_panel(self, parent):
        """PDFプレビューとコントロールを含むビューアパネルを生成します。

        Args:
            parent (tk.PanedWindow): このパネルを追加する親のPanedWindow。
        """
        viewer_frame = ttk.Frame(parent, padding=5)
        parent.add(viewer_frame, weight=4)

        # --- プレビュー上部のコントロール ---
        preview_controls_frame = ttk.Frame(viewer_frame)
        preview_controls_frame.pack(fill=tk.X)

        viewer_label = ttk.Label(preview_controls_frame, text="PDFプレビュー:")
        viewer_label.pack(side=tk.LEFT, anchor=tk.W)

        # --- ズームコントロール ---
        zoom_frame = ttk.Frame(preview_controls_frame)
        zoom_frame.pack(side=tk.LEFT, padx=20)

        zoom_out_btn = ttk.Button(zoom_frame, text="-", width=2)
        zoom_out_btn.pack(side=tk.LEFT, padx=5)
        scale_label = ttk.Label(zoom_frame, text="100%", width=5, anchor=tk.CENTER)
        scale_label.pack(side=tk.LEFT)
        zoom_in_btn = ttk.Button(zoom_frame, text="+", width=2)
        zoom_in_btn.pack(side=tk.LEFT, padx=5)

        # --- キャンバス ---
        canvas_container = ttk.Frame(viewer_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        canvas = tk.Canvas(canvas_container, bg="lightgray")
        canvas_vsb = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=canvas.yview)
        canvas_hsb = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=canvas.xview)
        canvas.configure(yscrollcommand=canvas_vsb.set, xscrollcommand=canvas_hsb.set)

        canvas_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.widgets.viewer_label = viewer_label
        self.widgets.zoom_out_btn = zoom_out_btn
        self.widgets.scale_label = scale_label
        self.widgets.zoom_in_btn = zoom_in_btn
        self.widgets.canvas = canvas
        self.widgets.canvas_vsb = canvas_vsb
        self.widgets.canvas_hsb = canvas_hsb

    def _create_statusbar(self):
        """ステータスバーを生成し、ルートウィンドウに配置します。"""
        status_bar = ttk.Label(self.root, text="準備完了", relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.widgets.status_bar = status_bar