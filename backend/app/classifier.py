import fitz

from .config import (
    TEXT_CHAR_THRESHOLD,
    IMAGE_RATIO_THRESHOLD,
    TABLE_COUNT_THRESHOLD,
    DRAWING_COUNT_THRESHOLD,
)


def classify_page(page):
    """
    Classifies a PDF page as TEXT or VISUAL.

    Classification rules:
    - text characters < 50
    - image ratio > 0.10
    - table count >= 1
    - drawing count > 30

    If any one of these conditions is true,
    the page is classified as VISUAL.
    """

    # -------------------------------------------------
    # 1. Count text characters
    # -------------------------------------------------
    text = page.get_text("text")
    text_chars = len(text.strip())

    # -------------------------------------------------
    # 2. Calculate image ratio
    # -------------------------------------------------
    page_area = page.rect.width * page.rect.height

    image_area = 0.0

    try:
        image_info = page.get_image_info()

        for image in image_info:
            bbox = image.get("bbox")

            if bbox:
                rect = fitz.Rect(bbox)
                image_area += rect.width * rect.height

    except Exception:
        image_area = 0.0

    if page_area > 0:
        image_ratio = image_area / page_area
    else:
        image_ratio = 0.0

    # -------------------------------------------------
    # 3. Count tables
    # -------------------------------------------------
    table_count = 0

    try:
        tables = page.find_tables()
        table_count = len(tables.tables)
    except Exception:
        table_count = 0

    # -------------------------------------------------
    # 4. Count drawings
    # -------------------------------------------------
    try:
        drawing_count = len(page.get_drawings())
    except Exception:
        drawing_count = 0

    # -------------------------------------------------
    # 5. Apply FARE classification rules
    # -------------------------------------------------
    is_visual = (
        text_chars < TEXT_CHAR_THRESHOLD
        or image_ratio > IMAGE_RATIO_THRESHOLD
        or table_count >= TABLE_COUNT_THRESHOLD
        or drawing_count > DRAWING_COUNT_THRESHOLD
    )

    if is_visual:
        page_type = "VISUAL"
    else:
        page_type = "TEXT"

    # -------------------------------------------------
    # 6. Return classification information
    # -------------------------------------------------
    return {
        "page_type": page_type,
        "text_chars": text_chars,
        "image_ratio": round(image_ratio, 4),
        "table_count": table_count,
        "drawing_count": drawing_count,
    }