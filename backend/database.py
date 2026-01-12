"""SQLite database connection and initialization."""

import sqlite3
import os
from pathlib import Path
from typing import Optional
from .config import DATA_DIR


def get_db_path() -> str:
    """Get the path to the SQLite database file."""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    return os.path.join(DATA_DIR, "consilience.db")


def get_connection() -> sqlite3.Connection:
    """
    Get a connection to the SQLite database.

    Returns:
        sqlite3.Connection: Database connection with row factory enabled
    """
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def init_db():
    """
    Initialize the database with required schema.
    Creates conversations and messages tables if they don't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Create conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Create messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT,
            stage_data TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
        )
    """)

    # Create index on conversation_id for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_conversation_id
        ON messages(conversation_id)
    """)

    conn.commit()
    conn.close()


# Initialize database on module import
init_db()
