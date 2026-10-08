import fitz

from .classifier import classify_page


def process_pdf(pdf_path):
    """
    Opens a PDF and classifies every page.

    Returns a list containing metadata
    for each page.
    """

    doc = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(doc, start=1):

        classification = classify_page(page)

        page_info = {
            "page_number": page_number,
            **classification
        }

        pages.append(page_info)

    doc.close()

    return pages