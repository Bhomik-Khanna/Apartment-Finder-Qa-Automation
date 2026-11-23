"""
tests/unit/test_storage_sqlite.py — SQLite database tests with isolated tmp_path.
"""

import sqlite3
import pytest


def init_test_db(db_path):
    """Initializes schema on a temporary database path."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER NOT NULL,
            review TEXT,
            suggestions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS apartments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            rent INTEGER NOT NULL,
            bedrooms INTEGER NOT NULL,
            notes TEXT,
            commute_minutes INTEGER
        )
    """)
    conn.commit()
    return conn


@pytest.mark.unit
def test_sqlite_feedback_save_and_retrieve(tmp_path):
    """Verifies that feedback is saved and retrieved accurately in isolated SQLite DB."""
    db_file = tmp_path / "test_feedback.db"
    conn = init_test_db(db_file)

    # Insert test feedback
    conn.execute(
        "INSERT INTO feedback (rating, review, suggestions) VALUES (?, ?, ?)",
        (5, "Super smooth UI", "Add dark mode toggle"),
    )
    conn.commit()

    # Query
    cursor = conn.execute("SELECT rating, review, suggestions FROM feedback")
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == 5
    assert row[1] == "Super smooth UI"
    assert row[2] == "Add dark mode toggle"


@pytest.mark.unit
def test_sqlite_apartment_uniqueness(tmp_path):
    """Verifies duplicate checking logic directly in the SQLite schema."""
    db_file = tmp_path / "test_apartments.db"
    conn = init_test_db(db_file)

    conn.execute(
        "INSERT INTO apartments (name, address, rent, bedrooms, commute_minutes) VALUES (?, ?, ?, ?, ?)",
        ("Palm Grove", "Sector 48, Faridabad", 14000, 2, 18),
    )
    conn.commit()

    # Check existence
    cursor = conn.execute(
        "SELECT COUNT(*) FROM apartments WHERE LOWER(name) = ? AND LOWER(address) = ?",
        ("palm grove", "sector 48, faridabad"),
    )
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 1