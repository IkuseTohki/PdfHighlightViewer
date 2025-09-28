"""エクスポート形式を定義する列挙型。"""

from enum import Enum

class ExportFormat(Enum):
    """サポートされているエクスポート形式。"""
    PNG = "png"
    PDF = "pdf"
    EXCEL = "excel"
