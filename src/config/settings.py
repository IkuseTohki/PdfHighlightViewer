"""設定ファイルの読み込みと管理を行います。"""

import configparser

class AppSettings:
    """setting.iniからアプリケーションの設定を読み込み、保持するクラス。

    このクラスは、設定ファイルが存在しない場合や、特定のキーが
    欠けている場合に備えて、フォールバック（デフォルト値）を提供します。

    Attributes:
        min_r (int): 検出対象の赤色の最小値 (0-255)。
        max_r (int): 検出対象の赤色の最大値 (0-255)。
        min_g (int): 検出対象の緑色の最小値 (0-255)。
        max_g (int): 検出対象の緑色の最大値 (0-255)。
        min_b (int): 検出対象の青色の最小値 (0-255)。
        max_b (int): 検出対象の青色の最大値 (0-255)。
        min_r_float (float): PyMuPDFで利用する赤色の最小値 (0.0-1.0)。
        max_r_float (float): PyMuPDFで利用する赤色の最大値 (0.0-1.0)。
        min_g_float (float): PyMuPDFで利用する緑色の最小値 (0.0-1.0)。
        max_g_float (float): PyMuPDFで利用する緑色の最大値 (0.0-1.0)。
        min_b_float (float): PyMuPDFで利用する青色の最小値 (0.0-1.0)。
        max_b_float (float): PyMuPDFで利用する青色の最大値 (0.0-1.0)。
        font_size (int): アプリケーションのデフォルトフォントサイズ。
    """
    def __init__(self, filepath="setting.ini"):
        """AppSettingsを初期化します。

        Args:
            filepath (str, optional): 読み込む設定ファイルのパス。
                Defaults to "setting.ini".
        """
        config = configparser.ConfigParser()
        config.read(filepath, encoding='utf-8')

        # --- 色設定の読み込み ---
        self.min_r = config.getint("ColorRange", "Min_R", fallback=200)
        self.max_r = config.getint("ColorRange", "Max_R", fallback=255)
        self.min_g = config.getint("ColorRange", "Min_G", fallback=200)
        self.max_g = config.getint("ColorRange", "Max_G", fallback=255)
        self.min_b = config.getint("ColorRange", "Min_B", fallback=0)
        self.max_b = config.getint("ColorRange", "Max_B", fallback=50)

        # PyMuPDFで利用するために0.0-1.0の範囲のフロート値に変換
        self.min_r_float = self.min_r / 255.0
        self.max_r_float = self.max_r / 255.0
        self.min_g_float = self.min_g / 255.0
        self.max_g_float = self.max_g / 255.0
        self.min_b_float = self.min_b / 255.0
        self.max_b_float = self.max_b / 255.0

        # --- UI設定の読み込み ---
        self.font_size = config.getint("UI", "font_size", fallback=10)

        # --- エクスポート設定の読み込み ---
        self.pdf_export_mode = config.get("Export", "PdfExportMode", fallback="one_page")
