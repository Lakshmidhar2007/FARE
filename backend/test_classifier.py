import fitz

from app.classifier import classify_page


# Create a temporary test PDF
pdf = fitz.open()

# -----------------------------------------
# Page 1: Text-heavy page
# -----------------------------------------
page1 = pdf.new_page()

text = """
FARE - Faithfulness and Abstention Rate Evaluation

This is a test page containing a large amount of
text. The page classifier should identify this page
as TEXT because it contains enough textual content
and does not contain tables, images, or many drawings.

The FARE system uses text pages for text-based
retrieval using BM25 and dense embeddings.
"""

page1.insert_text(
    (72, 72),
    text,
    fontsize=12
)


# -----------------------------------------
# Page 2: Mostly empty page
# -----------------------------------------
page2 = pdf.new_page()

page2.insert_text(
    (72, 72),
    "Visual page test",
    fontsize=12
)


# Save test PDF
pdf.save("test_document.pdf")
pdf.close()


# -----------------------------------------
# Open PDF and classify pages
# -----------------------------------------
doc = fitz.open("test_document.pdf")

for page_number, page in enumerate(doc, start=1):

    result = classify_page(page)

    print(f"\nPage {page_number}")
    print("-" * 30)
    print(f"Type          : {result['page_type']}")
    print(f"Text chars    : {result['text_chars']}")
    print(f"Image ratio   : {result['image_ratio']}")
    print(f"Table count   : {result['table_count']}")
    print(f"Drawing count : {result['drawing_count']}")

doc.close()