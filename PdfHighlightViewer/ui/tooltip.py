import tkinter as tk

class Tooltip:
    """ウィジェットにツールチップを追加するクラス。
    """
    def __init__(self, widget, text):
        """Tooltipオブジェクトを初期化します。

        Args:
            widget (tk.Widget): ツールチップを追加するウィジェット。
            text (str): ツールチップとして表示するテキスト。
        """
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.id = None
        self.x = self.y = 0
        self.enabled = False  # デフォルトでは無効
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        """マウスカーソルがウィジェットに入った際のイベントハンドラ。

        ツールチップが有効な場合、表示をスケジュールします。

        Args:
            event (tk.Event, optional): Tkinterから渡されるイベントオブジェクト。
                Defaults to None.
        """
        if self.enabled:
            self.schedule()

    def leave(self, event=None):
        """マウスカーソルがウィジェットから出た際のイベントハンドラ。

        ツールチップの表示スケジュールをキャンセルし、表示中の場合は非表示にします。

        Args:
            event (tk.Event, optional): Tkinterから渡されるイベントオブジェクト。
                Defaults to None.
        """
        self.unschedule()
        self.hidetip()

    def schedule(self):
        """ツールチップの表示をスケジュールします。

        既存のスケジュールがあればキャンセルし、指定ミリ秒後に表示処理を予約します。
        """
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        """ツールチップ表示のスケジュールをキャンセルします。
        """
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self):
        """ツールチップウィンドウを実際に作成して表示します。

        マウスカーソルの現在の位置に合わせて、ツールチップウィンドウを
        Toplevelウィンドウとして生成します。
        """
        if self.tooltip_window:
            return
        
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 1
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, justify='left',
                       background="#ffffe0", relief='solid', borderwidth=1,
                       font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        """表示されているツールチップウィンドウを破棄します。
        """
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()

    def enable(self):
        """このツールチップを有効化します。
        """
        self.enabled = True

    def disable(self):
        """このツールチップを無効化し、表示中の場合は非表示にします。
        """
        self.enabled = False
        self.hidetip()
