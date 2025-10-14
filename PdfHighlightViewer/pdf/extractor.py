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
                    if (app_settings.h_min_r_float <= r <= app_settings.h_max_r_float and
                        app_settings.h_min_g_float <= g <= app_settings.h_max_g_float and
                        app_settings.h_min_b_float <= b <= app_settings.h_max_b_float):
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
                if (app_settings.h_min_r_float <= r <= app_settings.h_max_r_float and
                    app_settings.h_min_g_float <= g <= app_settings.h_max_g_float and
                    app_settings.h_min_b_float <= b <= app_settings.h_max_b_float):
                    is_target_color = True
            
            # 線の色をチェック (まだ対象色と判定されていなければ)
            if not is_target_color:
                stroke_color = path.get("color")
                if stroke_color and len(stroke_color) == 3:
                    r, g, b = stroke_color
                    if (app_settings.h_min_r_float <= r <= app_settings.h_max_r_float and
                        app_settings.h_min_g_float <= g <= app_settings.h_max_g_float and
                        app_settings.h_min_b_float <= b <= app_settings.h_max_b_float):
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

def extract_colored_text_regions(doc, app_settings):
    """PDFドキュメントから指定された色の文字領域を検出します。

    Args:
        doc (fitz.Document): 解析対象のPDFドキュメント。
        app_settings (AppSettings): 抽出対象の色やUIの設定を含むオブジェクト。

    Returns:
        list: 検出された領域情報のタプルのリスト。[(page_num, rect), ...]
    """
    text_regions = []
    for page_num, page in enumerate(doc):
        # rawdict形式でテキスト情報を取得
        page_dict = page.get_text("rawdict")
        for block in page_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    # スパンの色情報を取得 (整数形式)
                    color_int = span.get("color")
                    if color_int is None:
                        continue

                    # 整数からRGB成分に変換
                    r = (color_int >> 16) & 0xFF
                    g = (color_int >> 8) & 0xFF
                    b = color_int & 0xFF

                    # 設定ファイルの色範囲と比較
                    if (app_settings.t_min_r <= r <= app_settings.t_max_r and
                        app_settings.t_min_g <= g <= app_settings.t_max_g and
                        app_settings.t_min_b <= b <= app_settings.t_max_b):
                        
                        rect = fitz.Rect(span["bbox"])
                        # 小さすぎるノイズのような領域は除外
                        if rect.width > 1 and rect.height > 1:
                            text_regions.append((page_num, rect))

    # TODO: 隣接するテキスト領域を結合して、より大きなまとまりにする処理を追加する
    #       現状では文字スパンごとに領域が分割されてしまうため。

    # 重複する領域を削除
    unique_regions = []
    seen_rects = set()
    for page_num, rect in text_regions:
        rect_tuple = (page_num, rect.x0, rect.y0, rect.x1, rect.y1)
        if rect_tuple not in seen_rects:
            unique_regions.append((page_num, rect))
            seen_rects.add(rect_tuple)

    return unique_regions

def extract_keyword_regions(doc, keyword):
    """PDFドキュメントから指定されたキーワードの領域を検出します。

    Args:
        doc (fitz.Document): 解析対象のPDFドキュメント。
        keyword (str): 検索するキーワード。

    Returns:
        list: 検出された領域情報のタプルのリスト。[(page_num, rect), ...]
    """
    keyword_regions = []
    if not keyword:
        return keyword_regions

    for page_num, page in enumerate(doc):
        # ページ内でキーワードを検索
        rects = page.search_for(keyword)
        for rect in rects:
            keyword_regions.append((page_num, rect))

    return keyword_regions