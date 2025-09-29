"""PDFから色付きの領域を検出する機能を提供します。"""

import fitz  # PyMuPDF

def extract_colored_regions(doc, app_settings):
    """PDFドキュメントから指定された色の領域を検出します。

    注釈、塗りつぶされた矩形、線で描かれた矩形の中から、設定ファイルで
    指定された色範囲に一致するものをすべて検索します。

    Args:
        doc (fitz.Document): 解析対象のPDFドキュメント。
        app_settings (AppSettings): 抽出対象の色やUIの設定を含むオブジェクト。

    Returns:
        list: 検出された領域情報のタプルのリスト。[(page_num, rect), ...]
    """
    highlights = []
    for page_num, page in enumerate(doc):
        # 方法1: 注釈ベースのハイライトを検出
        for annot in page.annots():
            if annot.type[0] == 8:  # 8はハイライト注釈
                colors = annot.colors
                stroke_color = colors.get('stroke') # ハイライトの色はstrokeで定義される
                if stroke_color and len(stroke_color) == 3:
                    r, g, b = stroke_color
                    if (app_settings.min_r_float <= r <= app_settings.max_r_float and
                        app_settings.min_g_float <= g <= app_settings.max_g_float and
                        app_settings.min_b_float <= b <= app_settings.max_b_float):
                        highlights.append((page_num, annot.rect))

        # 方法2: 描画ベースの矩形（塗りつぶし or 線）を検出
        drawings = page.get_drawings()
        for path in drawings:
            # 描画コマンドに矩形('re')が含まれているかチェック
            is_rect = any(item[0] == "re" for item in path.get("items", []))
            if not is_rect:
                continue

            is_target_color = False
            # 塗りつぶし色をチェック
            fill_color = path.get("fill")
            if fill_color and len(fill_color) == 3:
                r, g, b = fill_color
                if (app_settings.min_r_float <= r <= app_settings.max_r_float and
                    app_settings.min_g_float <= g <= app_settings.max_g_float and
                    app_settings.min_b_float <= b <= app_settings.max_b_float):
                    is_target_color = True
            
            # 線の色をチェック (まだ対象色と判定されていなければ)
            if not is_target_color:
                stroke_color = path.get("color")
                if stroke_color and len(stroke_color) == 3:
                    r, g, b = stroke_color
                    if (app_settings.min_r_float <= r <= app_settings.max_r_float and
                        app_settings.min_g_float <= g <= app_settings.max_g_float and
                        app_settings.min_b_float <= b <= app_settings.max_b_float):
                        is_target_color = True
            
            if is_target_color:
                # 小さすぎるノイズのような矩形は除外
                if path["rect"].width > 1 and path["rect"].height > 1:
                    highlights.append((page_num, path["rect"]))

    # 注釈と描画の両方で検出された場合など、重複する領域を削除
    unique_highlights = []
    seen_rects = set()
    for page_num, rect in highlights:
        # fitz.Rectはミュータブルでハッシュ化できないため、座標のタプルをキーにする
        rect_tuple = (page_num, rect.x0, rect.y0, rect.x1, rect.y1)
        if rect_tuple not in seen_rects:
            unique_highlights.append((page_num, rect))
            seen_rects.add(rect_tuple)

    return unique_highlights
