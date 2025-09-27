from PIL import Image, ImageTk

def render_page_to_image(page):
    """
    fitz.PageオブジェクトをTkinterで表示可能なPhotoImageに変換する。

    Args:
        page (fitz.Page): レンダリング対象のページ。

    Returns:
        (PIL.Image.Image, ImageTk.PhotoImage): PillowイメージとTkinterイメージのタプル。
    """
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    photo = ImageTk.PhotoImage(img)
    return img, photo
