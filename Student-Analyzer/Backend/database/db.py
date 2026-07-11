import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'placement.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cgpa REAL NOT NULL,
            experience INTEGER NOT NULL,
            level TEXT NOT NULL,
            goal TEXT,
            score INTEGER NOT NULL,
            category TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_report(name, cgpa, experience, level, goal, score, category):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, cgpa, experience, level, goal, score, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, cgpa, experience, level, goal, score, category))
    conn.commit()
    conn.close()

def get_student_by_name(search_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM students 
        WHERE name = ? COLLATE NOCASE
        ORDER BY timestamp DESC LIMIT 1
    ''', (search_name,))
    record = cursor.fetchone()
    conn.close()
    
    if record:
        return dict(record)
    else:
        return None