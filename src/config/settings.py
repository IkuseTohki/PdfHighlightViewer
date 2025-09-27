import configparser

class AppSettings:
    """
    setting.iniからアプリケーションの設定を読み込み、保持するクラス。
    """
    def __init__(self, filepath="setting.ini"):
        config = configparser.ConfigParser()
        config.read(filepath)

        # --- 色設定 ---
        self.min_r = config.getint("ColorRange", "Min_R", fallback=200)
        self.max_r = config.getint("ColorRange", "Max_R", fallback=255)
        self.min_g = config.getint("ColorRange", "Min_G", fallback=200)
        self.max_g = config.getint("ColorRange", "Max_G", fallback=255)
        self.min_b = config.getint("ColorRange", "Min_B", fallback=0)
        self.max_b = config.getint("ColorRange", "Max_B", fallback=50)

        self.min_r_float = self.min_r / 255.0
        self.max_r_float = self.max_r / 255.0
        self.min_g_float = self.min_g / 255.0
        self.max_g_float = self.max_g / 255.0
        self.min_b_float = self.min_b / 255.0
        self.max_b_float = self.max_b / 255.0

        # --- UI設定 ---
        self.font_size = config.getint("UI", "font_size", fallback=10)