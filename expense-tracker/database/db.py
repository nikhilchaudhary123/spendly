import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash


def get_db():
    db = sqlite3.connect('expense_tracker.db')
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def get_user_by_email(email):
    """Retrieve user by email address"""
    db = get_db()
    try:
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        return user
    finally:
        db.close()


def create_user(name, email, password):
    """Create a new user in the database"""
    db = get_db()
    try:
        hashed_password = generate_password_hash(password)
        cursor = db.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password)
        )
        db.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        db.close()


def init_db():
    db = get_db()

    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            category TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    db.commit()
    db.close()


def seed_db():
    db = get_db()

    existing_users = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if existing_users > 0:
        db.close()
        return

    password1 = generate_password_hash('password123')
    password2 = generate_password_hash('password456')
    password3 = generate_password_hash('password789')

    db.execute('''
        INSERT INTO users (name, email, password) VALUES (?, ?, ?)
    ''', ('John Doe', 'john@example.com', password1))

    db.execute('''
        INSERT INTO users (name, email, password) VALUES (?, ?, ?)
    ''', ('Jane Smith', 'jane@example.com', password2))

    db.execute('''
        INSERT INTO users (name, email, password) VALUES (?, ?, ?)
    ''', ('Bob Johnson', 'bob@example.com', password3))

    user1_id = db.execute('SELECT id FROM users WHERE email = ?', ('john@example.com',)).fetchone()['id']
    user2_id = db.execute('SELECT id FROM users WHERE email = ?', ('jane@example.com',)).fetchone()['id']

    base_date = datetime.now()

    sample_expenses = [
        (user1_id, 25.50, 'Lunch at cafe', 'food', (base_date - timedelta(days=1)).strftime('%Y-%m-%d')),
        (user1_id, 45.00, 'Uber ride to work', 'transport', (base_date - timedelta(days=2)).strftime('%Y-%m-%d')),
        (user1_id, 120.00, 'Monthly internet bill', 'utilities', (base_date - timedelta(days=5)).strftime('%Y-%m-%d')),
        (user1_id, 15.99, 'Netflix subscription', 'entertainment', (base_date - timedelta(days=7)).strftime('%Y-%m-%d')),
        (user1_id, 8.50, 'Coffee and pastry', 'food', base_date.strftime('%Y-%m-%d')),
        (user2_id, 35.00, 'Grocery shopping', 'food', (base_date - timedelta(days=1)).strftime('%Y-%m-%d')),
        (user2_id, 60.00, 'Gas station fill-up', 'transport', (base_date - timedelta(days=3)).strftime('%Y-%m-%d')),
        (user2_id, 150.00, 'Electric bill', 'utilities', (base_date - timedelta(days=10)).strftime('%Y-%m-%d')),
        (user2_id, 25.00, 'Movie tickets', 'entertainment', (base_date - timedelta(days=4)).strftime('%Y-%m-%d')),
        (user2_id, 12.00, 'Book purchase', 'entertainment', (base_date - timedelta(days=6)).strftime('%Y-%m-%d')),
    ]

    for expense in sample_expenses:
        db.execute('''
            INSERT INTO expenses (user_id, amount, description, category, date) VALUES (?, ?, ?, ?, ?)
        ''', expense)

    db.commit()
    db.close()
