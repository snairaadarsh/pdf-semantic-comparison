import os
import json
from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# ----------- Services -----------
from services.pdf_extractors import extract_text
from services.sentence_splitter import clean_text, split_into_sentences
from services.embedding import get_sentence_embeddings
from services.matcher import semantic_match

# ----------- Database -----------
from models.database import (
    init_db,
    save_report,
    get_all_reports,
    get_report_by_id
)

app = FastAPI()

# ----------- Init DB -----------
init_db()

# ----------- Templates & Static Files -----------
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------- Upload Directory -----------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================================
# ROUTES
# =========================================

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/compare")
async def compare(
    request: Request,
    title: str = Form(...),
    extractor: str = Form(...),   # pymupdf / pdfplumber / pdfminer
    model: str = Form(...),       # minilm (for now)
    pdfA: UploadFile = Form(...),
    pdfB: UploadFile = Form(...)
):
    # ---------- Save PDFs ----------
    pdfA_path = os.path.join(UPLOAD_DIR, pdfA.filename)
    pdfB_path = os.path.join(UPLOAD_DIR, pdfB.filename)

    with open(pdfA_path, "wb") as f:
        f.write(await pdfA.read())

    with open(pdfB_path, "wb") as f:
        f.write(await pdfB.read())

    # ---------- Extract Text (SAFE) ----------
    try:
        textA = extract_text(pdfA_path, extractor)
        textB = extract_text(pdfB_path, extractor)
    except Exception as e:
        return {
            "error": f"Text extraction failed using extractor '{extractor}'",
            "details": str(e)
        }

    # ---------- Validate Extraction ----------
    if not textA.strip() or not textB.strip():
        return {
            "error": "Empty text extracted",
            "message": f"Extractor '{extractor}' failed to extract text from one or both PDFs"
        }

    # ---------- Clean Text ----------
    cleanA = clean_text(textA)
    cleanB = clean_text(textB)

    # ---------- Sentence Splitting ----------
    sentencesA = split_into_sentences(cleanA)
    sentencesB = split_into_sentences(cleanB)

    # ---------- Validate Sentences ----------
    if len(sentencesA) == 0 or len(sentencesB) == 0:
        return {
            "error": "Sentence splitting failed",
            "message": "No valid sentences could be extracted after preprocessing"
        }

    # ---------- Sentence Embeddings ----------
    embA = get_sentence_embeddings(sentencesA, model)
    embB = get_sentence_embeddings(sentencesB, model)

    # ---------- Semantic Matching ----------
    result = semantic_match(
        sentencesA,
        sentencesB,
        embA,
        embB,
        threshold_low=0.65,
        threshold_high=0.85
    )

    # ---------- Save Report ----------
    save_report(
        title=title,
        pdfA=pdfA.filename,
        pdfB=pdfB.filename,
        extractor=extractor,
        model=model,
        result=result
    )

    # ---------- Final Output ----------
    return result


@app.get("/reports")
def reports(request: Request):
    reports = get_all_reports()
    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "reports": reports
        }
    )


@app.get("/report/{report_id}")
def view_report(request: Request, report_id: int):
    row = get_report_by_id(report_id)

    if row is None:
        return {"error": "Report not found"}

    title, result_json = row
    result = json.loads(result_json)

    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "title": title,
            "result": result
        }
    )
