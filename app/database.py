"""SQLite connection and schema helpers."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Generator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "students.db"


def get_database_path() -> Path:
    """Read the database path at runtime so tests can use a temporary database."""
    return Path(os.getenv("STUDENT_DB_PATH", str(DEFAULT_DB_PATH))).expanduser().resolve()


def connect_db() -> sqlite3.Connection:
    path = get_database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """FastAPI dependency that provides one connection per request."""
    conn = connect_db()
    try:
        yield conn
    finally:
        conn.close()


def initialize_database(db_path: str | Path | None = None) -> None:
    """Create the students table if it does not already exist."""
    path = Path(db_path).expanduser().resolve() if db_path else get_database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=10)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                course TEXT,
                address TEXT,
                enrollment_date TEXT,
                created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
                updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
