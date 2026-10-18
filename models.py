
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "marketing_copies.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS marketing_copies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                saved_at TEXT NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                description TEXT NOT NULL,
                audience TEXT NOT NULL,
                copy_type TEXT NOT NULL,
                generated_copy TEXT NOT NULL,
                tone_matches_brand_voice INTEGER NOT NULL,
                appropriate_length INTEGER NOT NULL,
                brand_keywords_included INTEGER NOT NULL
            )
        """)


def insert_copy(record):
    book = record["book"]
    checklist = record["checklist"]

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO marketing_copies (
                saved_at, title, author, genre, description, audience,
                copy_type, generated_copy, tone_matches_brand_voice,
                appropriate_length, brand_keywords_included
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            book["title"],
            book["author"],
            book["genre"],
            book["description"],
            book["audience"],
            record["format"],
            record["copy"],
            int(checklist["tone_matches_brand_voice"]),
            int(checklist["appropriate_length"]),
            int(checklist["brand_keywords_included"]),
        ))


def fetch_history():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT * FROM marketing_copies
            ORDER BY id DESC
        """).fetchall()

    return [dict(row) for row in rows]
