import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import fitz
from typing import Optional

from ..config.settings import Settings
from ..pdf import extractor, renderer
from ..export.exporter import Exporter
from ..export.formats import ExportFormat
from .ui_builder import UIBuilder
from .settings_window import SettingsWindow
from .tooltip import Tooltip

class MainWindow(tk.Tk):
    """アプリケーションのメインウィンドウとUIロジックを管理するクラス。
    """

    def __init__(self):
        """MainWindowオブジェクトを初期化します。

        ウィンドウのタイトル、サイズ、スタイル、状態変数、UIの構築など、
        アプリケーションの起動に必要な初期設定をすべて行います。
        """
        super().__init__()
        self.title("PDF Highlight Viewer")
        self.geometry("1200x800")
        
        self.settings = Settings()

        # --- スタイルとフォントの設定 ---
        default_font_family = 'Yu Gothic UI' 
        # フォントが存在しない場合に備えてフォールバックを設定
        available_fonts = font.families()
        if default_font_family not in available_fonts:
            default_font_family = 'TkDefaultFont'

        # ttkウィジェットのデフォルトフォントを設定
        style = ttk.Style()
        style.configure('.', font=(default_font_family, self.settings.font_size))
        
        # 標準tkウィジェットのデフォルトフォントを設定 (Listbox, Menuなど)
        self.option_add('*Font', (default_font_family, self.settings.font_size))

        # --- 状態変数 ---
        self.doc: Optional[fitz.Document] = None
        self.file_path_var = tk.StringVar()
        self.highlights = []
        self.page_images = {}
        self.current_page_num = -1
        self.scale = 1.0
        self.export_format = tk.StringVar(value=ExportFormat.PNG.value)
        self.platform = self.tk.call('tk', 'windowingsystem')

        # UIの構築と機能の割り当て
        self.builder = UIBuilder(self)
        self._bind_widgets()

        # 抽出ボタンにツールチップを設定
        self.extract_button_tooltip = Tooltip(
            self.builder.widgets.btn_extract, "抽出条件を1つ以上選択してください"
        )
        self.update_extract_button_state()

    def _bind_widgets(self):
        """UIウィジェットにイベントハンドラや変数を割り当てます。

        UIBuilderによって作成されたメニュー項目、ボタン、リストボックスなどの
        ウィジェットに、実行するコマンドや関連付ける変数を設定します。

        Note:
            この関数は内部利用を想定しています。
        """
        # --- メニュー ---
        self.builder.widgets.file_menu.add_command(label="PDFファイルを選択...", command=self.select_pdf_file)
        self.builder.widgets.file_menu.add_command(label="抽出を実行", command=self.run_extraction)
        self.builder.widgets.file_menu.add_command(label="設定...", command=self.open_settings_window)
        self.builder.widgets.file_menu.add_separator()
        self.builder.widgets.file_menu.add_command(label="終了", command=self.quit)

        for fmt in ExportFormat:
            self.builder.widgets.format_menu.add_radiobutton(
                label=fmt.value, variable=self.export_format, value=fmt.value)

        self.builder.widgets.export_menu.add_separator()
        self.builder.widgets.export_menu.add_command(label="選択中の領域をエクスポート...", command=self.export_selected)
        self.builder.widgets.export_menu.add_command(label="すべての領域をエクスポート...", command=self.export_all)

        # --- トップフレームのウィジェット ---
        self.builder.widgets.btn_extract.config(command=self.run_extraction)
        self.builder.widgets.btn_browse.config(command=self.select_pdf_file)
        self.builder.widgets.entry_filepath.config(textvariable=self.file_path_var)

        # --- リストボックス ---
        self.builder.widgets.listbox.bind("<<ListboxSelect>>", self.on_highlight_selected)

        # --- ズームボタン ---
        self.builder.widgets.zoom_in_btn.config(command=self.zoom_in)
        self.builder.widgets.zoom_out_btn.config(command=self.zoom_out)

        # --- キャンバスのスクロールイベント ---
        canvas = self.builder.widgets.canvas
        canvas.bind("<MouseWheel>", self._on_vertical_scroll)
        canvas.bind("<Shift-MouseWheel>", self._on_horizontal_scroll)
        canvas.bind("<Button-4>", self._on_vertical_scroll) # for Linux
        canvas.bind("<Button-5>", self._on_vertical_scroll) # for Linux
        # Linuxでの水平スクロール(Shift+Button-4/5)は環境依存性が高いため、
        # 一般的なShift+MouseWheelでカバーします。

    def select_pdf_file(self):
        """ファイル選択ダイアログを表示し、ユーザーが選択したPDFを読み込みます。

        ユーザーがファイルを選択すると、そのファイルのパスをUIに表示し、
        自動的に抽出処理を開始します。
        """
        filepath = filedialog.askopenfilename(
            title="PDFファイルを選択",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filepath:
            self.file_path_var.set(filepath)
            self.run_extraction()

    def run_extraction(self):
        """PDFファイルからハイライト領域の抽出処理を実行します。

        現在ファイルパス入力欄に表示されているPDFを読み込み、設定に基づいて
        ハイライト、文字色、キーワードなどの領域を抽出します。
        抽出結果はリストボックスに表示されます。
        """
        self.current_page_num = -1
        filepath = self.file_path_var.get()
        if not filepath:
            messagebox.showwarning("警告", "PDFファイルが選択されていません。")
            return

        # 既存のハイライト描画をクリア
        self.builder.widgets.canvas.delete("highlight_rect")

        try:
            self.doc = fitz.open(filepath)
            self.builder.widgets.status_bar.config(text=f"処理中: {filepath}")
            self.update()

            self.highlights = extractor.extract_regions(self.doc, self.settings)
            self.highlights.sort(key=lambda h: (h.page_num, h.rect.y0))

            self.page_images.clear()
            self.builder.widgets.listbox.delete(0, tk.END)

            if not self.highlights:
                messagebox.showinfo("情報", "指定された条件に一致する項目は見つかりませんでした。")
                if self.doc and self.doc.page_count > 0:
                    self.display_page(0)
                else:
                    self.builder.widgets.canvas.delete("all")
            else:
                for i, highlight in enumerate(self.highlights):
                    self.builder.widgets.listbox.insert(tk.END, f"項目 {i+1} (Page {highlight.page_num + 1})")
                self.builder.widgets.listbox.select_set(0)

            self.builder.widgets.status_bar.config(text="準備完了")

        except Exception as e:
            messagebox.showerror("エラー", f"ファイルの処理中にエラーが発生しました: {e}")
            self.builder.widgets.status_bar.config(text="エラー")

    def on_highlight_selected(self, event):
        """リストボックスで項目が選択されたときに呼び出されるイベントハンドラ。

        選択されたハイライト項目に対応するPDFのページを表示し、
        該当箇所に赤枠を描画してスクロールします。

        Args:
            event (tk.Event): Tkinterから渡されるイベントオブジェクト。
        """
        selected_indices = self.builder.widgets.listbox.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        
        def _update_display():
            """描画処理をまとめて実行する内部関数。"""
            highlight = self.highlights[selected_index]

            if highlight.page_num != self.current_page_num:
                self.current_page_num = highlight.page_num
                self.display_page(self.current_page_num)
            
            self.draw_highlight_rect(highlight.rect)
            self.scroll_to_rect(highlight.rect)

        self.after(1, _update_display)

    def display_page(self, page_num):
        """指定されたページ番号のPDFページをキャンバスに表示します。

        ページの画像がキャッシュにあればそれを使用し、なければ新しく
        レンダリングして表示します。表示倍率(scale)も考慮されます。

        Args:
            page_num (int): 表示するページの番号 (0-indexed)。
        """
        if self.doc is None:
            return

        if page_num not in self.page_images:
            pix = self.doc[page_num].get_pixmap(matrix=fitz.Matrix(self.scale, self.scale))
            self.page_images[page_num] = tk.PhotoImage(data=pix.tobytes("ppm"))
        
        self.builder.widgets.canvas.delete("all")
        self.builder.widgets.canvas.create_image(0, 0, anchor=tk.NW, image=self.page_images[page_num])
        self.builder.widgets.canvas.config(scrollregion=self.builder.widgets.canvas.bbox("all"))
        self.builder.widgets.scale_label.config(text=f"{self.scale*100:.0f}%")

    def draw_highlight_rect(self, rect):
        """指定された矩形領域にハイライト用の赤枠を描画します。

        既存の赤枠がある場合は一度削除してから、新しい枠を描画します。

        Args:
            rect (fitz.Rect): 赤枠を描画する座標。
        """
        self.builder.widgets.canvas.delete("highlight_rect")
        self.builder.widgets.canvas.create_rectangle(
            rect.x0 * self.scale, rect.y0 * self.scale,
            rect.x1 * self.scale, rect.y1 * self.scale,
            outline="red", width=self.settings.highlight_border_width, tags="highlight_rect"
        )

    def scroll_to_rect(self, rect):
        """指定された矩形領域がプレビュー画面の中央に来るようにスクロールします。

        Args:
            rect (fitz.Rect): スクロール先の目標となる座標。
        """
        canvas_height = self.builder.widgets.canvas.winfo_height()
        y_pos = rect.y0 * self.scale
        scroll_region = self.builder.widgets.canvas.bbox("all")
        if scroll_region and scroll_region[3] > 0:
            total_height = scroll_region[3]
            scroll_fraction = (y_pos - canvas_height / 2) / total_height
            self.builder.widgets.canvas.yview_moveto(max(0, scroll_fraction))

    def open_settings_window(self):
        """抽出条件などを変更するための設定ウィンドウを開きます。
        """
        SettingsWindow(self, self.settings)

    def export_selected(self):
        """現在選択中のハイライト領域を指定された形式でエクスポートします。
        """
        try:
            format_str = self.export_format.get()
            export_format = ExportFormat(format_str)
        except ValueError:
            messagebox.showerror("内部エラー", f"不明なエクスポート形式です: {format_str}")
            return

        exporter = Exporter(
            doc=self.doc,
            highlights=self.highlights,
            app_settings=self.settings
        )
        exporter.export_selected(export_format=export_format, listbox=self.builder.widgets.listbox)

    def export_all(self):
        """抽出されたすべてのハイライト領域を指定された形式でエクスポートします。
        """
        try:
            format_str = self.export_format.get()
            export_format = ExportFormat(format_str)
        except ValueError:
            messagebox.showerror("内部エラー", f"不明なエクスポート形式です: {format_str}")
            return
            
        exporter = Exporter(
            doc=self.doc,
            highlights=self.highlights,
            app_settings=self.settings
        )
        exporter.export_all(export_format=export_format)
        
    def zoom_in(self):
        """PDFプレビューの表示倍率を上げて再描画します。
        """
        if not self.doc or self.current_page_num == -1: return
        if self.scale >= 5.0: return
        self.scale += 0.1
        self.page_images.clear()
        self.display_page(self.current_page_num)
        if self.highlights and self.builder.widgets.listbox.curselection():
            self.draw_highlight_rect(self.highlights[self.builder.widgets.listbox.curselection()[0]].rect)

    def zoom_out(self):
        """PDFプレビューの表示倍率を下げて再描画します。
        """
        if not self.doc or self.current_page_num == -1: return
        if self.scale <= 0.2: return
        self.scale -= 0.1
        self.page_images.clear()
        self.display_page(self.current_page_num)
        if self.highlights and self.builder.widgets.listbox.curselection():
            self.draw_highlight_rect(self.highlights[self.builder.widgets.listbox.curselection()[0]].rect)

    def update_extract_button_state(self):
        """抽出ボタンの有効/無効状態を、現在の抽出条件に応じて更新します。

        抽出条件が1つも選択されていない場合はボタンを無効化し、
        ツールチップでその旨をユーザーに伝えます。
        """
        is_any_condition_selected = (
            self.settings.extract_highlights or
            self.settings.extract_text_color or
            self.settings.extract_keyword
        )

        if is_any_condition_selected:
            self.builder.widgets.btn_extract.config(state=tk.NORMAL)
            self.extract_button_tooltip.disable()
        else:
            self.builder.widgets.btn_extract.config(state=tk.DISABLED)
            self.extract_button_tooltip.enable()

    def _on_vertical_scroll(self, event):
        """キャンバスの垂直スクロールをマウスホイールと連動させます。

        プラットフォーム間のイベントの違いを吸収します。

        Args:
            event (tk.Event): マウスホイールイベント。
        """
        if self.platform == "win32":
            self.builder.widgets.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif self.platform == "x11": # Linux
            if event.num == 4:
                self.builder.widgets.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.builder.widgets.canvas.yview_scroll(1, "units")
        else: # macOS
            self.builder.widgets.canvas.yview_scroll(int(-1 * event.delta), "units")

    def _on_horizontal_scroll(self, event):
        """キャンバスの水平スクロールをShift+マウスホイールと連動させます。

        プラットフォーム間のイベントの違いを吸収します。

        Args:
            event (tk.Event): マウスホイールイベント。
        """
        if self.platform == "win32":
            self.builder.widgets.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        elif self.platform == "x11": # Linux (Shift+Button-4/5)
             # Linuxの水平スクロールは環境差が大きいため、ここでは基本的な実装に留めます
            if event.num == 4:
                self.builder.widgets.canvas.xview_scroll(-1, "units")
            elif event.num == 5:
                self.builder.widgets.canvas.xview_scroll(1, "units")
        else: # macOS
            self.builder.widgets.canvas.xview_scroll(int(-1 * event.delta), "units")


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()