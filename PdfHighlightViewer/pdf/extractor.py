import fitz
from collections import defaultdict

class Highlight:
    """抽出された領域の情報を格納するデータクラス。"""
    def __init__(self, page_num, rect):
        """Highlightオブジェクトを初期化します。

        Args:
            page_num (int): 領域が存在するページ番号 (0-indexed)。
            rect (fitz.Rect): 領域の座標。
        """
        self.page_num = page_num
        self.rect = rect

    def __repr__(self):
        """Highlightオブジェクトの公式な文字列表現を返します。

        Returns:
            str: オブジェクトのデバッグ用文字列表現。
        """
        return f"Highlight(Page {self.page_num}, Rect{self.rect})"

def extract_regions(doc, settings):
    """設定に基づいて、PDFから複数の条件を組み合わせて領域を抽出します。

    指定された複数の抽出条件（ハイライト色、文字色、キーワード）をAND条件
    として扱い、すべての条件を満たす領域を抽出します。

    Args:
        doc (fitz.Document): 解析対象のPDFドキュメント。
        settings (Settings): 抽出条件を含むアプリケーション設定オブジェクト。

    Returns:
        list[Highlight]: 抽出された領域を表すHighlightオブジェクトのリスト。
    """
    extract_highlights = settings.extract_highlights
    extract_text_color = settings.extract_text_color
    extract_keyword = settings.extract_keyword
    
    num_of_conditions = sum([extract_highlights, extract_text_color, extract_keyword])

    if num_of_conditions == 0:
        return []

    highlight_rects = _extract_colored_regions(doc, settings) if extract_highlights else None
    text_color_rects = _extract_colored_text_regions(doc, settings) if extract_text_color else None
    keyword_rects = _extract_keyword_regions(doc, settings.extraction_keyword) if extract_keyword else None

    base_rects = []
    if extract_keyword:
        base_rects = keyword_rects
    elif extract_text_color:
        base_rects = text_color_rects
    elif extract_highlights:
        base_rects = highlight_rects

    if num_of_conditions == 1:
        return [Highlight(page_num, rect) for page_num, rect in base_rects]

    highlights_by_page = defaultdict(list)
    if highlight_rects is not None:
        for page_num, rect in highlight_rects:
            highlights_by_page[page_num].append(rect)

    text_color_by_page = defaultdict(list)
    if text_color_rects is not None:
        for page_num, rect in text_color_rects:
            text_color_by_page[page_num].append(rect)

    final_results = []
    for page_num, base_rect in base_rects:
        is_valid = True

        if extract_highlights and base_rects is not highlight_rects:
            is_contained_in_highlight = any(h_rect.intersects(base_rect) for h_rect in highlights_by_page[page_num])
            if not is_contained_in_highlight:
                is_valid = False
        
        if is_valid and extract_text_color and base_rects is not text_color_rects:
            is_intersecting_colored_text = any(base_rect.intersects(c_rect) for c_rect in text_color_by_page[page_num])
            if not is_intersecting_colored_text:
                is_valid = False
        
        if is_valid:
            final_results.append(Highlight(page_num, base_rect))
            
    return final_results

def _extract_colored_regions(doc, settings):
    """PDFから指定された色の図形や注釈領域を抽出します。

    設定で指定された色範囲に一致する、長方形の図形（drawings）や
    ハイライト注釈（annotations）の領域を検出します。

    Note:
        この関数は内部利用を想定しています。

    Args:
        doc (fitz.Document): 解析対象のPDFドキュメント。
        settings (Settings): ハイライト色の範囲設定を含むオブジェクト。

    Returns:
        list[tuple[int, fitz.Rect]]: ページ番号と領域の座標(Rect)の
            タプルからなるリスト。
    """
    highlights = []
    h_min_r, h_min_g, h_min_b = settings.highlight_color_min
    h_max_r, h_max_g, h_max_b = settings.highlight_color_max

    for page_num, page in enumerate(doc):
        for annot in page.annots():
            if annot.type[0] == 8:
                colors = annot.colors
                stroke_color = colors.get('stroke')
                if stroke_color and len(stroke_color) == 3:
                    r, g, b = [int(c * 255) for c in stroke_color]
                    if (h_min_r <= r <= h_max_r and
                        h_min_g <= g <= h_max_g and
                        h_min_b <= b <= h_max_b):
                        highlights.append((page_num, annot.rect))

        drawings = page.get_drawings()
        for path in drawings:
            is_rect = any(item[0] == "re" for item in path.get("items", []))
            if not is_rect:
                continue

            is_target_color = False
            fill_color = path.get("fill")
            if fill_color and len(fill_color) == 3:
                r, g, b = [int(c * 255) for c in fill_color]
                if (h_min_r <= r <= h_max_r and
                    h_min_g <= g <= h_max_g and
                    h_min_b <= b <= h_max_b):
                    is_target_color = True
            
            if not is_target_color:
                stroke_color = path.get("color")
                if stroke_color and len(stroke_color) == 3:
                    r, g, b = [int(c * 255) for c in stroke_color]
                    if (h_min_r <= r <= h_max_r and
                        h_min_g <= g <= h_max_g and
                        h_min_b <= b <= h_max_b):
                        is_target_color = True
            
            if is_target_color:
                if path["rect"].width > 1 and path["rect"].height > 1:
                    highlights.append((page_num, path["rect"]))

    unique_highlights = []
    seen_rects = set()
    for page_num, rect in highlights:
        rect_tuple = (page_num, rect.x0, rect.y0, rect.x1, rect.y1)
        if rect_tuple not in seen_rects:
            unique_highlights.append((page_num, rect))
            seen_rects.add(rect_tuple)

    return unique_highlights

def _extract_colored_text_regions(doc, settings):
    """PDFから指定された色の文字が含まれる領域を抽出します。

    設定で指定された色範囲に一致する文字（span）を検出し、
    その文字が含まれる領域を返します。

    Note:
        この関数は内部利用を想定しています。

    Args:
        doc (fitz.Document): 解析対象のPDFドキュメント。
        settings (Settings): 文字色の範囲設定を含むオブジェクト。

    Returns:
        list[tuple[int, fitz.Rect]]: ページ番号と領域の座標(Rect)の
            タプルからなるリスト。
    """
    text_regions = []
    t_min_r, t_min_g, t_min_b = settings.text_color_min
    t_max_r, t_max_g, t_max_b = settings.text_color_max

    for page_num, page in enumerate(doc):
        page_dict = page.get_text("rawdict")
        for block in page_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    color_int = span.get("color")
                    if color_int is None:
                        continue

                    r = (color_int >> 16) & 0xFF
                    g = (color_int >> 8) & 0xFF
                    b = color_int & 0xFF

                    if (t_min_r <= r <= t_max_r and
                        t_min_g <= g <= t_max_g and
                        t_min_b <= b <= t_max_b):
                        
                        rect = fitz.Rect(span["bbox"])
                        if rect.width > 1 and rect.height > 1:
                            text_regions.append((page_num, rect))

    unique_regions = []
    seen_rects = set()
    for page_num, rect in text_regions:
        rect_tuple = (page_num, rect.x0, rect.y0, rect.x1, rect.y1)
        if rect_tuple not in seen_rects:
            unique_regions.append((page_num, rect))
            seen_rects.add(rect_tuple)

    return unique_regions

def _extract_keyword_regions(doc, keyword):
    """PDFから指定されたキーワードが含まれる領域を抽出します。

    PyMuPDFの `search_for` メソッドを利用して、指定されたキーワードが
    出現するすべての領域を検出します。

    Note:
        この関数は内部利用を想定しています。

    Args:
        doc (fitz.Document): 解析対象のPDFドキュメント。
        keyword (str): 検索するキーワード。空文字列の場合は何も返しません。

    Returns:
        list[tuple[int, fitz.Rect]]: ページ番号と領域の座標(Rect)の
            タプルからなるリスト。
    """
    keyword_regions = []
    if not keyword:
        return keyword_regions

    for page_num, page in enumerate(doc):
        rects = page.search_for(keyword)
        for rect in rects:
            keyword_regions.append((page_num, rect))

    return keyword_regions
