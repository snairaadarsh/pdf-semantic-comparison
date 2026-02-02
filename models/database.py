import sqlite3
from datetime import datetime
import json

DB_PATH = "database.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            pdf_a_name TEXT,
            pdf_b_name TEXT,
            extractor TEXT,
            model TEXT,
            result_json TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_report(title, pdfA, pdfB, extractor, model, result):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reports 
        (title, pdf_a_name, pdf_b_name, extractor, model, result_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        pdfA,
        pdfB,
        extractor,
        model,
        json.dumps(result),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


def get_all_reports():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, pdf_a_name, pdf_b_name, model, extractor, created_at
        FROM reports
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_report_by_id(report_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT title, result_json
        FROM reports
        WHERE id = ?
    """, (report_id,))
    row = cur.fetchone()
    conn.close()
    return row
