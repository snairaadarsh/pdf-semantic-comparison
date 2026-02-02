import fitz  # PyMuPDF
import pdfplumber
from pdfminer.high_level import extract_text


# -------- PyMuPDF --------
def extract_text_pymupdf(pdf_path: str) -> str:
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text


# -------- PDFPlumber --------
def extract_text_pdfplumber(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text



# -------- PDFMiner (SAFE) --------
def extract_text_pdfminer(pdf_path: str) -> str:
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"[PDFMiner ERROR] {e}")
        return ""

# -------- Dispatcher --------
def extract_text(pdf_path: str, extractor: str) -> str:
    if extractor == "pymupdf":
        return extract_text_pymupdf(pdf_path)

    elif extractor == "pdfplumber":
        return extract_text_pdfplumber(pdf_path)

    elif extractor == "pdfminer":
        return extract_text_pdfminer(pdf_path)

    else:
        raise ValueError(f"Unknown extractor: {extractor}")
