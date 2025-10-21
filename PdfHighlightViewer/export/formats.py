"""エクスポート形式を定義する列挙型。"""

from enum import Enum

class ExportFormat(Enum):
    """サポートされているエクスポート形式。"""
    PNG = "png"
    PDF = "pdf"
    EXCEL = "excel"

class PdfExportMode(Enum):
    """PDFエクスポートのモードを定義する列挙型。"""
    ONE_PAGE = "one_page"
    MERGE = "merge"
