import json
from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .pdf_processor import process_pdf


# -------------------------------------------------
# FARE Application
# -------------------------------------------------

app = FastAPI(
    title="FARE API",
    description="Faithfulness & Abstention Rate Evaluation",
    version="0.1.0"
)


# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Data directories
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
META_DIR = DATA_DIR / "meta"

PDF_DIR.mkdir(parents=True, exist_ok=True)
META_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "fare"
    }


# -------------------------------------------------
# Upload PDF
# -------------------------------------------------

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Check file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Generate unique document ID
    doc_id = str(uuid.uuid4())

    # Get safe filename
    filename = Path(file.filename).name

    # Location where PDF will be saved
    pdf_path = PDF_DIR / f"{doc_id}_{filename}"

    # Save uploaded PDF
    with pdf_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -------------------------------------------------
    # Process PDF pages
    # -------------------------------------------------

    try:
        pages = process_pdf(pdf_path)

    except Exception as exc:

        # Remove invalid PDF if processing fails
        pdf_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=f"Could not process PDF: {exc}"
        )

    # -------------------------------------------------
    # Save document metadata
    # -------------------------------------------------

    metadata = {
        "doc_id": doc_id,
        "filename": filename,
        "pdf_path": str(pdf_path),
        "total_pages": len(pages),
        "pages": pages
    }

    metadata_path = META_DIR / f"{doc_id}.json"

    with metadata_path.open("w", encoding="utf-8") as metadata_file:
        json.dump(
            metadata,
            metadata_file,
            indent=2
        )

    # -------------------------------------------------
    # Count page types
    # -------------------------------------------------

    text_pages = sum(
        1
        for page in pages
        if page["page_type"] == "TEXT"
    )

    visual_pages = sum(
        1
        for page in pages
        if page["page_type"] == "VISUAL"
    )

    # -------------------------------------------------
    # Return upload result
    # -------------------------------------------------

    return {
        "doc_id": doc_id,
        "filename": filename,
        "total_pages": len(pages),
        "text_pages": text_pages,
        "visual_pages": visual_pages,
        "pages": pages
    }