#!/usr/bin/env python3
"""Simple DB inspector for campus.db

Run from project root:
    python3 scripts/db_inspect.py

It prints tables, schema for `users`, row count and up to 20 sample rows.
"""
import sqlite3
from pathlib import Path
import sys

DB = Path("campus.db")
if not DB.exists():
    print(f"Error: {DB} not found in current directory: {Path.cwd()}")
    sys.exit(1)

conn = sqlite3.connect(str(DB))
cur = conn.cursor()

print("Connected to:", DB)

# list tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
rows = cur.fetchall()
tables = [r[0] for r in rows]
print("\nTables:")
for t in tables:
    print(" -", t)

if 'users' not in tables:
    print("\nNo table named 'users' found. Exiting.")
    conn.close()
    sys.exit(0)

# show schema for users
print("\nSchema for 'users':")
cur.execute("PRAGMA table_info('users');")
cols = cur.fetchall()
# PRAGMA returns: cid, name, type, notnull, dflt_value, pk
for c in cols:
    cid, name, ctype, notnull, dflt, pk = c
    print(f"  {name} ({ctype}) notnull={bool(notnull)} pk={bool(pk)} default={dflt}")

# row count
cur.execute("SELECT COUNT(*) FROM users;")
count = cur.fetchone()[0]
print(f"\nRow count in users: {count}")

# sample rows
limit = 20
print(f"\nFirst {limit} rows from users (columns shown above):")
cur.execute(f"SELECT * FROM users LIMIT {limit};")
rows = cur.fetchall()
if not rows:
    print("  (no rows)")
else:
    # print rows with indexes
    for i, r in enumerate(rows, start=1):
        print(f"\n  Row {i}:")
        for col_value, col_meta in zip(r, cols):
            name = col_meta[1]
            print(f"    {name}: {col_value}")

conn.close()
print("\nDone.")
