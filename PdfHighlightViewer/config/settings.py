"""設定ファイルの読み込みと管理を行います。"""

import configparser

class AppSettings:
    """setting.iniからアプリケーションの設定を読み込み、保持するクラス。

    このクラスは、設定ファイルが存在しない場合や、特定のキーが
    欠けている場合に備えて、フォールバック（デフォルト値）を提供します。
    """
    def __init__(self, filepath="setting.ini"):
        """AppSettingsを初期化します。

        Args:
            filepath (str, optional): 読み込む設定ファイルのパス。
                Defaults to "setting.ini".
        """
        config = configparser.ConfigParser()
        config.read(filepath, encoding='utf-8')

        # --- ハイライト色設定の読み込み ---
        self.h_min_r = config.getint("HighlightColor", "Min_R", fallback=200)
        self.h_max_r = config.getint("HighlightColor", "Max_R", fallback=255)
        self.h_min_g = config.getint("HighlightColor", "Min_G", fallback=200)
        self.h_max_g = config.getint("HighlightColor", "Max_G", fallback=255)
        self.h_min_b = config.getint("HighlightColor", "Min_B", fallback=0)
        self.h_max_b = config.getint("HighlightColor", "Max_B", fallback=50)

        # PyMuPDFのハイライト検出で利用するために0.0-1.0の範囲のフロート値に変換
        self.h_min_r_float = self.h_min_r / 255.0
        self.h_max_r_float = self.h_max_r / 255.0
        self.h_min_g_float = self.h_min_g / 255.0
        self.h_max_g_float = self.h_max_g / 255.0
        self.h_min_b_float = self.h_min_b / 255.0
        self.h_max_b_float = self.h_max_b / 255.0

        # --- 文字色設定の読み込み (0-255の整数値) ---
        self.t_min_r = config.getint("TextColor", "Min_R", fallback=200)
        self.t_max_r = config.getint("TextColor", "Max_R", fallback=255)
        self.t_min_g = config.getint("TextColor", "Min_G", fallback=0)
        self.t_max_g = config.getint("TextColor", "Max_G", fallback=50)
        self.t_min_b = config.getint("TextColor", "Min_B", fallback=0)
        self.t_max_b = config.getint("TextColor", "Max_B", fallback=50)

        # --- UI設定の読み込み ---
        self.font_size = config.getint("UI", "font_size", fallback=10)

        # --- エクスポート設定の読み込み ---
        self.pdf_export_mode = config.get("Export", "PdfExportMode", fallback="one_page")
        self.excel_image_scale = config.getfloat("Export", "ExcelImageScale", fallback=2.0)
