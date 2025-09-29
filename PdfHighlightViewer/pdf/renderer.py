"""PDFページのレンダリング機能を提供します。"""

import fitz
from PIL import Image, ImageTk

def render_page_to_image(page, scale=1.0):
    """fitz.PageオブジェクトをTkinterで表示可能なPhotoImageに変換します。

    Args:
        page (fitz.Page): レンダリング対象のページ。
        scale (float, optional): 表示倍率。デフォルトは1.0。

    Returns:
        (Image.Image, ImageTk.PhotoImage): PillowイメージとTkinterイメージのタプル。
            Pillowイメージは後続の処理で、Tkinterイメージは表示に利用できます。
    """
    # 指定された倍率でレンダリングするためのMatrixを作成
    matrix = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=matrix)
    
    # PyMuPDFのPixmapオブジェクトからPillowのImageオブジェクトを作成
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # PillowのImageオブジェクトをTkinterのPhotoImageオブジェクトに変換
    photo = ImageTk.PhotoImage(img)
    return img, photo
