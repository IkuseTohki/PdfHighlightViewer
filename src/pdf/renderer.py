import fitz
from PIL import Image, ImageTk

def render_page_to_image(page, scale=1.0):
    """
    fitz.PageオブジェクトをTkinterで表示可能なPhotoImageに変換する。

    Args:
        page (fitz.Page): レンダリング対象のページ。
        scale (float): 表示倍率。

    Returns:
        (PIL.Image.Image, ImageTk.PhotoImage): PillowイメージとTkinterイメージのタプル。
    """
    # 指定された倍率でレンダリングするためのMatrixを作成
    matrix = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=matrix)
    
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    photo = ImageTk.PhotoImage(img)
    return img, photo