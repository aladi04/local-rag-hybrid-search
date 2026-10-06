from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile, File
from ingestion.pipeline import ingest_pdf


router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    document_id = str(uuid4())
    
    file_path = UPLOAD_DIR / f"{uuid4()}.pdf"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = ingest_pdf(pdf_path=file_path, document_id=document_id, filename=file.filename)
    
    return {
        "filename": file.filename, 
        "message": "File uploaded successfully",
        **result
        }