import sqlite3
import os
from datetime import datetime

# Define where the database file will be stored
DB_PATH = os.path.join("data", "voice_bot.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            account_number TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')

    # 2. FAQs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')

    # 3. NEW: Interaction Logs Table (For Analytics)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_text TEXT,
            intent TEXT,
            bot_reply TEXT,
            response_time REAL
        )
    ''')

    # Seed Data (Only if empty)
    cursor.execute('SELECT count(*) FROM users')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, account_number, balance) VALUES ('John Doe', '123456789', 5400.50)")
        cursor.execute("INSERT INTO faqs (question, answer) VALUES ('hours', 'We are open from 9 AM to 5 PM, Monday to Friday.')")
        cursor.execute("INSERT INTO faqs (question, answer) VALUES ('location', 'Our head office is located in Mumbai, near CST station.')")
        cursor.execute("INSERT INTO faqs (question, answer) VALUES ('contact', 'You can reach support at support@voicebot.com.')")
        conn.commit()
        
    conn.close()

# --- Helper Functions ---

def get_user_balance(username="John Doe"):
    conn = get_db_connection()
    result = conn.execute("SELECT balance FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return result["balance"] if result else None

def get_faq_answer(keyword):
    conn = get_db_connection()
    result = conn.execute("SELECT answer FROM faqs WHERE question LIKE ?", (f'%{keyword}%',)).fetchone()
    conn.close()
    return result["answer"] if result else None

def log_interaction(user_text, intent, bot_reply, response_time):
    """Saves the conversation to the database."""
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO logs (user_text, intent, bot_reply, response_time) VALUES (?, ?, ?, ?)",
        (user_text, intent, bot_reply, response_time)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()