import fitz  # PyMuPDF

def extract_yellow_regions(doc):
    """
    PDFドキュメントから黄色い領域（注釈、塗りつぶし、線）を検出する。

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

        # 方法2: 描画ベースの黄色い矩形（塗りつぶし or 線）
        drawings = page.get_drawings()
        for path in drawings:
            is_rect = any(item[0] == "re" for item in path.get("items", []))
            if not is_rect:
                continue

            is_yellow = False
            # 塗りつぶし色をチェック
            fill_color = path.get("fill")
            if fill_color and len(fill_color) == 3:
                r, g, b = fill_color
                if r > 0.8 and g > 0.8 and b < 0.2:
                    is_yellow = True
            
            # 線の色をチェック (まだ黄色と判定されていなければ)
            if not is_yellow:
                stroke_color = path.get("color")
                if stroke_color and len(stroke_color) == 3:
                    r, g, b = stroke_color
                    if r > 0.8 and g > 0.8 and b < 0.2:
                        is_yellow = True
            
            if is_yellow:
                if path["rect"].width > 1 and path["rect"].height > 1:
                    highlights.append((page_num, path["rect"]))

    # 重複する可能性のある領域を削除
    unique_highlights = []
    seen_rects = set()
    for page_num, rect in highlights:
        # fitz.Rectはハッシュ化できないため、座標のタプルをキーにする
        rect_tuple = (page_num, rect.x0, rect.y0, rect.x1, rect.y1)
        if rect_tuple not in seen_rects:
            unique_highlights.append((page_num, rect))
            seen_rects.add(rect_tuple)

    return unique_highlights