# PDF Semantic Comparison Tool

A local PDF comparison tool that compares two PDF documents based on semantic meaning rather than exact text matching.  
The application uses transformer-based sentence embeddings to identify similar content, paraphrases, and missing sections between documents.

---

## Features

- Semantic comparison of two PDF files
- Sentence-level similarity analysis
- Detection of:
  - Semantic matches
  - Paraphrased content
  - Missing or unmatched content
- Multiple PDF text extraction options:
  - PyMuPDF
  - PDFPlumber
  - PDFMiner
- Multiple embedding models:
  - MiniLM
  - DistilBERT
  - SBERT
- Cosine similarity–based scoring
- Local SQLite database for storing comparison reports
- Web interface built with FastAPI and Jinja templates

---

## Project Structure
pdf_semantic_compare/
│
├── app.py # FastAPI application entry point
├── requirements.txt # Python dependencies
├── database.db # Local SQLite database
│
├── services/ # Core logic modules
│ ├── pdf_extractors.py
│ ├── sentence_splitter.py
│ ├── embedding.py
│ └── matcher.py
│
├── models/ # Database utilities
│ └── database.py
│
├── templates/ # HTML templates
│ ├── base.html
│ ├── index.html
│ ├── edit.html
│ └── report.html
│
├── static/ # Static assets
│ └── style.css
│
├── uploads/ # Uploaded PDF files
└── venv/ # Local virtual environment

## How It Works

1.Upload two PDF files

2.Selected extractor converts PDFs to text

3.Text is cleaned and split into sentences

4.Sentences are embedded using the selected transformer model

5.Cosine similarity is computed between sentence pairs

6.Results are classified as matches, paraphrases, or no matches

7.Reports are saved locally and can be viewed later

## Notes

-The application runs entirely locally
-Performance depends on PDF size and selected embedding model
-Larger models (e.g. SBERT) may require more system memory
