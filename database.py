import sqlite3


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Создаем таблицу пользователей
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        balance INTEGER DEFAULT 1000
    )
    ''')

    # Создаем таблицу транзакций
    cur.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        cost INTEGER NOT NULL,
        description TEXT
    )
    ''')

    conn.commit()
    conn.close()


def add_user(name, login, password):
    conn = get_db_connection()
    cur = conn.cursor()

    # СОХРАНЕНИЕ ПОЛЬЗОВАТЕЛЯ ЧЕРЕЗ cur.execute
    cur.execute('''
    INSERT INTO users (name, login, password, balance)
    VALUES (?, ?, ?, ?)
    ''', (name, login, password, 1000))

    user_id = cur.lastrowid
    conn.commit()
    conn.close()

    return user_id


def get_user_by_login(login):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE login = ?', (login,))
    user = cur.fetchone()

    conn.close()
    return user


def authenticate_user(login, password):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password))
    user = cur.fetchone()

    conn.close()
    return user


def get_user_balance(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    result = cur.fetchone()

    conn.close()
    return result['balance'] if result else 0


def update_balance(user_id, amount, trans_type, description):
    conn = get_db_connection()
    cur = conn.cursor()

    # Обновляем баланс
    cur.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))

    # Добавляем транзакцию
    cur.execute('''
    INSERT INTO transactions (user_id, type, cost, description)
    VALUES (?, ?, ?, ?)
    ''', (user_id, trans_type, abs(amount), description))

    conn.commit()
    conn.close()
    return True


def get_user_transactions(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
    SELECT * FROM transactions 
    WHERE user_id = ? 
    ORDER BY id DESC 
    LIMIT 10
    ''', (user_id,))

    transactions = cur.fetchall()
    conn.close()
    return transactions