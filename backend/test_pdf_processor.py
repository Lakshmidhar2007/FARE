from app.pdf_processor import process_pdf


pdf_path = "test_document.pdf"

pages = process_pdf(pdf_path)

print("\nPDF PROCESSING RESULT")
print("=" * 40)

for page in pages:
    print(f"Page {page['page_number']}")
    print(f"  Type          : {page['page_type']}")
    print(f"  Text chars    : {page['text_chars']}")
    print(f"  Image ratio   : {page['image_ratio']}")
    print(f"  Table count   : {page['table_count']}")
    print(f"  Drawing count : {page['drawing_count']}")
    print()