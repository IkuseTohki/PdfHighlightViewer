import configparser
import os

class Settings:
    """
    設定を管理するシングルトンクラス。
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, config_file='setting.ini'):
        """
        Args:
            config_file (str, optional): 設定ファイル名。 Defaults to 'setting.ini'.
        """
        if self.initialized:
            return
        self.initialized = True

        self.config = configparser.ConfigParser()
        self.config_file = config_file
        
        # デフォルト値の設定
        self.set_default_values()
        
        if os.path.exists(self.config_file):
            self.load()
        else:
            self.save()

    def set_default_values(self):
        """各種設定のデフォルト値を設定します。
        """
        # UI設定
        self.highlight_border_width = 3
        self.font_size = 10
        
        # 色の範囲設定
        self.highlight_color_min = (200, 200, 0)
        self.highlight_color_max = (255, 255, 50)
        self.text_color_min = (200, 0, 0)
        self.text_color_max = (255, 50, 50)

        # 抽出設定
        self.extract_highlights = True
        self.extract_text_color = False
        self.extract_keyword = False
        self.extraction_keyword = ""

        # エクスポート設定
        self.pdf_export_mode = "one_page"
        self.excel_image_scale = 2.0
        self.image_export_border_width = 5
        self.pdf_export_border_width = 1.5

    def load(self):
        """設定ファイルから設定を読み込みます。
        """
        self.config.read(self.config_file, 'utf-8')

        # UI設定
        self.highlight_border_width = self.config.getint('UI', 'HighlightBorderWidth', fallback=3)
        self.font_size = self.config.getint('UI', 'FontSize', fallback=10)

        # 色の範囲設定
        min_r_h = self.config.getint('HighlightColor', 'Min_R', fallback=200)
        max_r_h = self.config.getint('HighlightColor', 'Max_R', fallback=255)
        min_g_h = self.config.getint('HighlightColor', 'Min_G', fallback=200)
        max_g_h = self.config.getint('HighlightColor', 'Max_G', fallback=255)
        min_b_h = self.config.getint('HighlightColor', 'Min_B', fallback=0)
        max_b_h = self.config.getint('HighlightColor', 'Max_B', fallback=50)
        self.highlight_color_min = (min_r_h, min_g_h, min_b_h)
        self.highlight_color_max = (max_r_h, max_g_h, max_b_h)

        min_r_t = self.config.getint('TextColor', 'Min_R', fallback=200)
        max_r_t = self.config.getint('TextColor', 'Max_R', fallback=255)
        min_g_t = self.config.getint('TextColor', 'Min_G', fallback=0)
        max_g_t = self.config.getint('TextColor', 'Max_G', fallback=50)
        min_b_t = self.config.getint('TextColor', 'Min_B', fallback=0)
        max_b_t = self.config.getint('TextColor', 'Max_B', fallback=50)
        self.text_color_min = (min_r_t, min_g_t, min_b_t)
        self.text_color_max = (max_r_t, max_g_t, max_b_t)

        # 抽出設定
        self.extract_highlights = self.config.getboolean('Extraction', 'ExtractHighlights', fallback=True)
        self.extract_text_color = self.config.getboolean('Extraction', 'ExtractTextColor', fallback=False)
        self.extract_keyword = self.config.getboolean('Extraction', 'ExtractKeyword', fallback=False)
        self.extraction_keyword = self.config.get('Extraction', 'Keyword', fallback="")

        # エクスポート設定
        self.pdf_export_mode = self.config.get('Export', 'PdfExportMode', fallback='one_page')
        self.excel_image_scale = self.config.getfloat('Export', 'ExcelImageScale', fallback=2.0)
        self.image_export_border_width = self.config.getint('Export', 'ImageExportBorderWidth', fallback=5)
        self.pdf_export_border_width = self.config.getfloat('Export', 'PdfExportBorderWidth', fallback=1.5)

    def save(self):
        """現在の設定を設定ファイルに保存します。
        """
        if not self.config.has_section('UI'):
            self.config.add_section('UI')
        self.config.set('UI', 'HighlightBorderWidth', str(self.highlight_border_width))
        self.config.set('UI', 'FontSize', str(self.font_size))

        if not self.config.has_section('HighlightColor'):
            self.config.add_section('HighlightColor')
        self.config.set('HighlightColor', 'Min_R', str(self.highlight_color_min[0]))
        self.config.set('HighlightColor', 'Max_R', str(self.highlight_color_max[0]))
        self.config.set('HighlightColor', 'Min_G', str(self.highlight_color_min[1]))
        self.config.set('HighlightColor', 'Max_G', str(self.highlight_color_max[1]))
        self.config.set('HighlightColor', 'Min_B', str(self.highlight_color_min[2]))
        self.config.set('HighlightColor', 'Max_B', str(self.highlight_color_max[2]))

        if not self.config.has_section('TextColor'):
            self.config.add_section('TextColor')
        self.config.set('TextColor', 'Min_R', str(self.text_color_min[0]))
        self.config.set('TextColor', 'Max_R', str(self.text_color_max[0]))
        self.config.set('TextColor', 'Min_G', str(self.text_color_min[1]))
        self.config.set('TextColor', 'Max_G', str(self.text_color_max[1]))
        self.config.set('TextColor', 'Min_B', str(self.text_color_min[2]))
        self.config.set('TextColor', 'Max_B', str(self.text_color_max[2]))

        if not self.config.has_section('Extraction'):
            self.config.add_section('Extraction')
        self.config.set('Extraction', 'ExtractHighlights', str(self.extract_highlights))
        self.config.set('Extraction', 'ExtractTextColor', str(self.extract_text_color))
        self.config.set('Extraction', 'ExtractKeyword', str(self.extract_keyword))
        self.config.set('Extraction', 'Keyword', self.extraction_keyword)

        if not self.config.has_section('Export'):
            self.config.add_section('Export')
        self.config.set('Export', 'PdfExportMode', self.pdf_export_mode)
        self.config.set('Export', 'ExcelImageScale', str(self.excel_image_scale))
        self.config.set('Export', 'ImageExportBorderWidth', str(self.image_export_border_width))
        self.config.set('Export', 'PdfExportBorderWidth', str(self.pdf_export_border_width))

        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def save_extraction_settings(self):
        """抽出関連の設定のみを設定ファイルに保存します。
        """
        # self.config を直接使わず、ファイルを読み込み直して更新する
        config = configparser.ConfigParser()
        # 既存のファイルを読み込むことで、他のセクションの値を維持する
        if os.path.exists(self.config_file):
            config.read(self.config_file, 'utf-8')

        if not config.has_section('Extraction'):
            config.add_section('Extraction')
        config.set('Extraction', 'ExtractHighlights', str(self.extract_highlights))
        config.set('Extraction', 'ExtractTextColor', str(self.extract_text_color))
        config.set('Extraction', 'ExtractKeyword', str(self.extract_keyword))
        config.set('Extraction', 'Keyword', self.extraction_keyword)

        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
