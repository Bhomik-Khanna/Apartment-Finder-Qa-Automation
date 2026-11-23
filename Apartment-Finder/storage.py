"""
storage.py

ONE job: save and load apartments using SQLite instead of JSON.

Swapping JSON for SQLite required changing only this file —
nothing in app.py, tracker.py, or the page files changed at all.
That's the separation of concerns we built from day one paying off.

Database: apartments.db (created automatically on first run)
Tables:
  - apartments: all listing data
  - feedback:   user ratings and reviews from the AI assistant
  - apt_requests: new apartment submissions from the AI assistant
"""

import sqlite3
import os
from apartment import Apartment

DB_FILE = "apartments.db"


def get_connection():
    """Get a database connection, creating the DB and tables if needed."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    _create_tables(conn)
    return conn


def _create_tables(conn):
    """Create all tables if they don't already exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS apartments (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            address         TEXT NOT NULL,
            rent            INTEGER NOT NULL,
            bedrooms        INTEGER NOT NULL,
            notes           TEXT DEFAULT '',
            commute_minutes REAL,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            rating      INTEGER NOT NULL,
            review      TEXT,
            suggestions TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS apt_requests (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            address     TEXT NOT NULL,
            rent        INTEGER,
            bedrooms    INTEGER,
            notes       TEXT,
            status      TEXT DEFAULT 'pending',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    



def save_to_file(apartments, filepath=None):
    """
    Save a list of Apartment objects to SQLite.
    filepath param kept for backward compatibility — ignored.
    Replaces all existing apartments with the new list.
    """
    conn = get_connection()
    try:
        # Clear existing and reinsert — keeps it simple and consistent
        conn.execute("DELETE FROM apartments")
        for apt in apartments:
            conn.execute("""
                INSERT INTO apartments (name, address, rent, bedrooms, notes, commute_minutes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (apt.name, apt.address, apt.rent, apt.bedrooms,
                  apt.notes or "", apt.commute_minutes))
        conn.commit()
    finally:
        conn.close()


def load_from_file(filepath=None):
    """
    Load all apartments from SQLite and return as Apartment objects.
    filepath param kept for backward compatibility — ignored.
    Returns empty list if DB doesn't exist yet.
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM apartments ORDER BY id"
        ).fetchall()
        return [
            Apartment(
                name=           row["name"],
                address=        row["address"],
                rent=           row["rent"],
                bedrooms=       row["bedrooms"],
                notes=          row["notes"],
                commute_minutes=row["commute_minutes"],
            )
            for row in rows
        ]
    finally:
        conn.close()


def apartment_exists(name, address):
    """
    Check if an apartment with the same name AND address already exists.
    Used for duplicate detection in the Manage page.
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id FROM apartments WHERE LOWER(name) = LOWER(?) AND LOWER(address) = LOWER(?)",
            (name.strip(), address.strip())
        ).fetchone()
        return row is not None
    finally:
        conn.close()




def save_feedback(rating, review, suggestions):
    """Save a feedback entry from the AI assistant."""
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO feedback (rating, review, suggestions)
            VALUES (?, ?, ?)
        """, (rating, review or "", suggestions or ""))
        conn.commit()
        return True
    except Exception as e:
        print(f"Feedback save error: {e}")
        return False
    finally:
        conn.close()


def load_feedback():
    """Load all feedback entries. Used by the analytics dashboard."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM feedback ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()




def save_apt_request(name, address, rent, bedrooms, notes):
    """Save a new apartment request submitted via the AI assistant."""
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO apt_requests (name, address, rent, bedrooms, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (name, address, rent or 0, bedrooms or 0, notes or ""))
        conn.commit()
        return True
    except Exception as e:
        print(f"Apt request save error: {e}")
        return False
    finally:
        conn.close()


def load_apt_requests(status="pending"):
    """Load apartment requests by status. Used by admin panel."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM apt_requests WHERE status = ? ORDER BY submitted_at DESC",
            (status,)
        ).fetchall()
        return [dict(row) for row in rows] if rows else []
    except Exception:
        return []
    finally:
        conn.close()



def migrate_from_json():
    """
    One-time migration: if apartments.json exists, import it into SQLite
    then rename it so we don't import twice.
    Run this once, then it's done.
    """
    import json

    json_file = "apartments.json"
    if not os.path.exists(json_file):
        return

    print(f"Migrating {json_file} → SQLite...")
    try:
        with open(json_file, "r") as f:
            data = json.load(f)

        apartments = [
            Apartment(
                name=           d["name"],
                address=        d["address"],
                rent=           d["rent"],
                bedrooms=       d["bedrooms"],
                notes=          d.get("notes", ""),
                commute_minutes=d.get("commute_minutes"),
            )
            for d in data
        ]
        save_to_file(apartments)
        os.rename(json_file, json_file + ".migrated")
        print(f"Migrated {len(apartments)} apartments. {json_file} → {json_file}.migrated")
    except Exception as e:
        print(f"Migration error: {e}")



migrate_from_json()