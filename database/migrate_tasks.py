#!/usr/bin/env python3
"""Create tasks table and seed initial data if missing.

This script is safe to run multiple times. It will:
- Create the tasks table if it does not exist
- Insert a couple of seed rows only if the table is empty

It uses the existing myapp.db located in this directory to maintain consistency
with other tools (db_shell.py, db_visualizer/sqlite.env, and db_connection.txt).
"""

import os
import sqlite3
from datetime import datetime

DB_NAME = "myapp.db"

# PUBLIC_INTERFACE
def ensure_tasks_table(conn: sqlite3.Connection) -> None:
    """Create the tasks table if it doesn't exist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

# PUBLIC_INTERFACE
def seed_tasks_if_empty(conn: sqlite3.Connection) -> int:
    """Seed initial tasks if the table is empty. Returns number of rows inserted."""
    cur = conn.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()[0] or 0
    if count > 0:
        return 0

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    seeds = [
        ("Buy groceries", 0, now, now),
        ("Read a book", 0, now, now),
    ]
    for title, completed, created_at, updated_at in seeds:
        conn.execute(
            "INSERT INTO tasks (title, completed, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, completed, created_at, updated_at),
        )
    return len(seeds)

def main() -> None:
    """Run migration/initialization for tasks table."""
    db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
    # Ensure we operate on the exact same DB file used elsewhere
    conn = sqlite3.connect(db_path)
    try:
        ensure_tasks_table(conn)
        inserted = seed_tasks_if_empty(conn)
        conn.commit()
        print(f"Tasks migration complete. Seed rows inserted: {inserted}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
