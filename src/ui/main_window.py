import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import fitz

from pdf import extractor, renderer

class MainWindow:
    """
    アプリケーションのメインウィンドウとUIロジックを管理する。
    """
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Highlight Viewer")
        self.root.geometry("1200x800")

        # --- 状態変数 ---
        self.doc = None
        self.highlights = []
        self.page_images = []
        self.current_page_num = -1
        self.current_highlight_rect = None
        self.scale = 1.0

        self._setup_ui()

    def _setup_ui(self):
        """GUIウィジェットの初期化と配置を行う。"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 5))

        self.btn_open = ttk.Button(top_frame, text="PDFを開く", command=self.open_pdf_file)
        self.btn_open.pack(side=tk.LEFT)

        self.lbl_filepath = ttk.Label(top_frame, text="PDFファイルが選択されていません", anchor=tk.W)
        self.lbl_filepath.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        content_frame = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)

        list_frame = ttk.Frame(content_frame, padding=5)
        content_frame.add(list_frame, weight=1)

        list_label = ttk.Label(list_frame, text="検出された黄色い領域:")
        list_label.pack(anchor=tk.W)
        
        listbox_container = ttk.Frame(list_frame)
        listbox_container.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        self.listbox = tk.Listbox(listbox_container)
        self.listbox_sby = ttk.Scrollbar(listbox_container, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.listbox_sby.set)
        self.listbox.bind("<<ListboxSelect>>", self.on_list_select)
        
        self.listbox_sby.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        viewer_frame = ttk.Frame(content_frame, padding=5)
        content_frame.add(viewer_frame, weight=4)

        # --- プレビューとズームコントロール --- #
        preview_controls_frame = ttk.Frame(viewer_frame)
        preview_controls_frame.pack(fill=tk.X)

        viewer_label = ttk.Label(preview_controls_frame, text="PDFプレビュー:")
        viewer_label.pack(side=tk.LEFT, anchor=tk.W)

        zoom_frame = ttk.Frame(preview_controls_frame)
        zoom_frame.pack(side=tk.LEFT, padx=20)

        zoom_out_btn = ttk.Button(zoom_frame, text="-", command=self.zoom_out, width=2)
        zoom_out_btn.pack(side=tk.LEFT, padx=5)
        self.scale_label = ttk.Label(zoom_frame, text=f"{self.scale*100:.0f}%")
        self.scale_label.pack(side=tk.LEFT)
        zoom_in_btn = ttk.Button(zoom_frame, text="+", command=self.zoom_in, width=2)
        zoom_in_btn.pack(side=tk.LEFT, padx=5)

        canvas_container = ttk.Frame(viewer_frame)
        canvas_container.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        self.canvas = tk.Canvas(canvas_container, bg="lightgray")
        self.canvas_vsb = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas_hsb = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.canvas_vsb.set, xscrollcommand=self.canvas_hsb.set)

        self.canvas_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def open_pdf_file(self):
        filepath = filedialog.askopenfilename(
            title="PDFファイルを選択",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not filepath:
            return

        self._reset_state()
        self.lbl_filepath.config(text=filepath)

        try:
            self.doc = fitz.open(filepath)
            self.highlights = extractor.extract_yellow_regions(self.doc)
            self._populate_listbox()
            if self.doc.page_count > 0:
                self.show_page(0)
        except Exception as e:
            messagebox.showerror("エラー", f"PDFの処理中にエラーが発生しました:\n{e}")
            self.lbl_filepath.config(text=f"エラー: {e}")

    def _reset_state(self):
        self.listbox.delete(0, tk.END)
        self.canvas.delete("all")
        self.highlights = []
        self.page_images = []
        self.current_page_num = -1
        self.current_highlight_rect = None
        self.scale = 1.0
        if self.doc:
            self.doc.close()

    def _populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, (page_num, rect) in enumerate(self.highlights):
            self.listbox.insert(tk.END, f"領域 {i + 1} (Page {page_num + 1})")

    def on_list_select(self, event):
        selection_indices = self.listbox.curselection()
        if not selection_indices:
            return
        
        selected_index = selection_indices[0]
        
        if 0 <= selected_index < len(self.highlights):
            page_num, rect = self.highlights[selected_index]
            self.current_highlight_rect = rect
            self.show_page(page_num, highlight_rect=rect)

    def show_page(self, page_num, highlight_rect=None):
        if not self.doc or not (0 <= page_num < self.doc.page_count):
            return

        self.current_page_num = page_num
        page = self.doc[page_num]
        img, photo = renderer.render_page_to_image(page, scale=self.scale)
        
        self.page_images.append(photo)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        if highlight_rect:
            self.canvas.create_rectangle(
                highlight_rect.x0 * self.scale,
                highlight_rect.y0 * self.scale,
                highlight_rect.x1 * self.scale,
                highlight_rect.y1 * self.scale,
                outline="red",
                width=3,
                tags="highlight"
            )
            page_height = self.canvas.bbox(tk.ALL)[3]
            if page_height > 0:
                self.canvas.yview_moveto((highlight_rect.y0 * self.scale) / page_height)

    def zoom_in(self):
        """表示倍率を上げて再描画する。"""
        self.scale += 0.1
        self.scale_label.config(text=f"{self.scale*100:.0f}%")
        self.show_page(self.current_page_num, highlight_rect=self.current_highlight_rect)

    def zoom_out(self):
        """表示倍率を下げて再描画する。"""
        if self.scale > 0.2: # 10%以下にはしない
            self.scale -= 0.1
            self.scale_label.config(text=f"{self.scale*100:.0f}%")
            self.show_page(self.current_page_num, highlight_rect=self.current_highlight_rect)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()