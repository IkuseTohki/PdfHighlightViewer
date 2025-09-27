import fitz  # PyMuPDF

def extract_yellow_regions(doc):
    """
    PDFドキュメントから黄色い領域（注釈および描画）を検出する。

    Args:
        doc (fitz.Document): 解析対象のPDFドキュメント。

    Returns:
        list: 検出された領域情報のタプルのリスト。[(page_num, rect), ...]
    """
    highlights = []
    for page_num, page in enumerate(doc):
        # 方法1: 注釈ベースのハイライト
        for annot in page.annots():
            if annot.type[0] == 8:  # 8はハイライト
                colors = annot.colors
                if colors.get('stroke') and len(colors['stroke']) == 3 and colors['stroke'][0] > 0.8 and colors['stroke'][1] > 0.8 and colors['stroke'][2] < 0.2:
                    highlights.append((page_num, annot.rect))

        # 方法2: 描画ベースの黄色い矩形
        drawings = page.get_drawings()
        for path in drawings:
            is_rect_fill = False
            if path["type"] == "f":
                for item in path["items"]:
                    if item[0] == "re":
                        is_rect_fill = True
                        break
            if not is_rect_fill: continue
            
            fill_color = path.get("fill")
            if fill_color and len(fill_color) == 3:
                r, g, b = fill_color
                if r > 0.8 and g > 0.8 and b < 0.2:
                    if path["rect"].width > 1 and path["rect"].height > 1:
                        highlights.append((page_num, path["rect"]))
    return highlights
