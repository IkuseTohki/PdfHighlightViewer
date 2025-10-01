"""アプリケーションのメインウィンドウとUIの振る舞いを定義します。"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import fitz
from typing import Optional

from config.settings import AppSettings
from pdf import extractor, renderer
from export.exporter import Exporter
from export.formats import ExportFormat
from .ui_builder import UIBuilder

class MainWindow:
    """アプリケーションのメインウィンドウとUIロジックを管理するクラス。"""

    def __init__(self, root):
        """MainWindowを初期化します。

        Args:
            root (tk.Tk): Tkinterのルートウィンドウ。
        """
        self.root = root
        self.root.title("PDF Highlight Viewer")
        self.root.geometry("1200x800")

        # --- 状態変数 ---
        self.doc: Optional[fitz.Document] = None
        self.current_filepath: Optional[str] = None
        self.filepath_var = tk.StringVar() # UIのEntryウィジェットと連動
        self.highlights = []
        self.page_images = []
        self.current_page_num = -1
        self.current_highlight_rect = None
        self.scale = 1.0
        self.app_settings = AppSettings()
        self.export_format = tk.StringVar(value=ExportFormat.PNG.value)
        self.extraction_mode = tk.StringVar(value="highlight")  # 抽出モード（"highlight" or "text"）

        # UIの構築をUIBuilderに委譲
        self.ui = UIBuilder(self.root, self)
        self.ui.setup()

        self._apply_styles()

    def _apply_styles(self):
        """設定ファイルに基づいてUIのスタイル（フォントサイズなど）を適用します。"""
        font_size = self.app_settings.font_size
        default_font = ("TkDefaultFont", font_size)
        
        style = ttk.Style()
        style.configure(".", font=default_font)
        
        self.ui.listbox.config(font=default_font)
        self.ui.scale_label.config(font=default_font)

    def select_pdf_file(self):
        """ファイルダイアログを開き、処理対象のPDFファイルを選択します。"""
        filepath = filedialog.askopenfilename(
            title="PDFファイルを選択",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not filepath:
            return

        # 新しいファイルが選択されたので、現在の表示をリセット
        self._reset_state()
        self.root.update_idletasks() # リセットをUIに即時反映
        self.filepath_var.set(filepath)


    def run_extraction(self):
        """現在選択されているPDFファイルに対して抽出処理を実行します。"""
        self.current_filepath = self.filepath_var.get()
        if not self.current_filepath:
            messagebox.showwarning("ファイル未選択", "ファイルパスを入力するか、「参照...」ボタンからPDFファイルを選択してください。")
            return

        # 抽出の都度、前回の結果をクリアし、UIに即時反映
        self._reset_state()
        self.root.update_idletasks()

        try:
            self.doc = fitz.open(self.current_filepath)

            mode = self.extraction_mode.get()
            if mode == "highlight":
                self.highlights = extractor.extract_colored_regions(self.doc, self.app_settings)
            elif mode == "text":
                self.highlights = extractor.extract_colored_text_regions(self.doc, self.app_settings)
            else:
                self.highlights = []
                messagebox.showerror("内部エラー", f"不明な抽出モードです: {mode}")

            if not self.highlights:
                messagebox.showinfo("抽出結果", "指定された条件に一致する領域は見つかりませんでした。")

            self._populate_listbox()
            
            # ページを表示
            if self.doc.page_count > 0:
                # 最初のハイライトがあればそのページを表示
                if self.highlights:
                    self.show_page(self.highlights[0][0])

        except Exception as e:
            messagebox.showerror("エラー", f"PDFの処理中にエラーが発生しました:\n{e}")
            self.filepath_var.set(f"エラー: {e}")


    def _reset_state(self):
        """抽出結果やプレビューなど、アプリケーションの状態をリセットします。"""
        self.ui.listbox.delete(0, tk.END)
        self.highlights = []
        self.page_images = []
        self.current_page_num = -1
        self.current_highlight_rect = None
        self.scale = 1.0
        if self.doc:
            self.doc.close()
            self.doc = None
        # self.current_filepath, self.filepath_var はここではリセットしない

    def _populate_listbox(self):
        """検出した領域のリストをリストボックスに表示します。"""
        self.ui.listbox.delete(0, tk.END)
        for i, (page_num, rect) in enumerate(self.highlights):
            self.ui.listbox.insert(tk.END, f"領域 {i + 1} (Page {page_num + 1})")

    def on_list_select(self, event):
        """リストボックスの項目が選択されたときに呼び出されるイベントハンドラです。"""
        selection_indices = self.ui.listbox.curselection()
        if not selection_indices:
            return
        
        selected_index = selection_indices[0]
        
        if 0 <= selected_index < len(self.highlights):
            page_num, rect = self.highlights[selected_index]
            self.current_highlight_rect = rect
            self.show_page(page_num, highlight_rect=rect)

    def show_page(self, page_num, highlight_rect=None):
        """指定されたページをキャンバスに表示し、指定領域をハイライトします。"""
        if not self.doc or not (0 <= page_num < self.doc.page_count):
            # PDFが開かれていない場合、キャンバスをクリアする
            self.ui.canvas.delete("all")
            return

        self.current_page_num = page_num
        page = self.doc[page_num]
        img, photo = renderer.render_page_to_image(page, scale=self.scale)
        
        self.page_images.append(photo)

        self.ui.canvas.delete("all")
        self.ui.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.ui.canvas.config(scrollregion=self.ui.canvas.bbox(tk.ALL))

        if highlight_rect:
            self.ui.canvas.create_rectangle(
                highlight_rect.x0 * self.scale,
                highlight_rect.y0 * self.scale,
                highlight_rect.x1 * self.scale,
                highlight_rect.y1 * self.scale,
                outline="red",
                width=3,
                tags="highlight"
            )
            # スクロール位置の計算と移動
            canvas_height = self.ui.canvas.winfo_height()
            page_height = self.ui.canvas.bbox(tk.ALL)[3]
            if page_height > 0:
                # ハイライトが中央に来るようにスクロール
                scroll_pos = (highlight_rect.y0 * self.scale - canvas_height / 2) / page_height
                self.ui.canvas.yview_moveto(max(0, scroll_pos))


    def _get_export_format_enum(self) -> Optional[ExportFormat]:
        """現在のエクスポート形式をEnumとして取得します。不正な場合はエラー表示してNoneを返します。"""
        try:
            return ExportFormat(self.export_format.get())
        except ValueError:
            messagebox.showerror("内部エラー", "不明なエクスポート形式が選択されています。")
            return None

    def export_selected_highlight(self):
        """選択されたハイライトのエクスポート処理をExporterに委譲します。"""
        export_format_enum = self._get_export_format_enum()
        if not export_format_enum:
            return

        exporter = Exporter(self.doc, self.highlights, self.ui.listbox, self.app_settings)
        exporter.export_selected(export_format_enum)

    def export_all_highlights(self):
        """すべてのハイライトのエクスポート処理をExporterに委譲します。"""
        export_format_enum = self._get_export_format_enum()
        if not export_format_enum:
            return

        exporter = Exporter(self.doc, self.highlights, self.ui.listbox, self.app_settings)
        exporter.export_all(export_format_enum)

    def zoom_in(self):
        """表示倍率を上げて再描画します。"""
        if not self.doc: return
        if self.scale >= 5.0: # 500%を上限とする
            return
        self.scale += 0.1
        # 浮動小数点数の誤差を考慮し、上限を超えた場合は500%に設定
        if self.scale > 5.0:
            self.scale = 5.0
        self.ui.scale_label.config(text=f"{self.scale*100:.0f}%")
        self.show_page(self.current_page_num, highlight_rect=self.current_highlight_rect)

    def zoom_out(self):
        """表示倍率を下げて再描画します。"""
        if not self.doc: return
        if self.scale > 0.2:
            self.scale -= 0.1
            self.ui.scale_label.config(text=f"{self.scale*100:.0f}%")
            self.show_page(self.current_page_num, highlight_rect=self.current_highlight_rect)