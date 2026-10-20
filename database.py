import mysql.connector
from mysql.connector import Error
import os

from werkzeug.security import generate_password_hash, check_password_hash

DB_HOST = "185.114.247.43"
DB_PORT = 3306
DB_NAME = "sch688_vvedenie"
DB_USER = "sch688_vvedenie"
DB_PASS = "Qwerty123"


def get_db_connection():
    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return cnx
    except Error as e:
        print(f"Ошибка подкл MySQL: {e}")
        return None


def init_db():
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        balance INT DEFAULT 1000,
        credits INT DEFAULT 1000,
        surname VARCHAR(100) NOT NULL,
        lastname VARCHAR(100) NULL,
        total_spent DOUBLE DEFAULT 0,
        total_deposited DOUBLE DEFAULT 0,
        is_admin TINYINT(1) DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        type VARCHAR(20) NOT NULL,
        cost INT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    cursor.close()
    conn.close()


def add_user(username, email, password, surname, lastname=None):
    """
    Создаёт пользователя.

    username  — уникальный логин (столбец users.username)
    email     — уникальный, NOT NULL (столбец users.email)
    password  — СЫРОЙ пароль, хэшируется здесь
    surname   — NOT NULL
    lastname  — необязательный
    """
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            print(f"Пользователь с логином {username} уже существует")
            return None

        cursor.execute('''
            INSERT INTO users (username, email, password_hash, surname, lastname,
                               balance, credits)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            username,
            email,
            generate_password_hash(password),
            surname,
            lastname,
            1000,
            1000,
        ))

        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except Error as e:
        print(f"Ошибка добавления юзера: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_user_by_login(username):
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user





def authenticate_user(username, password):
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if user and check_password_hash(user['password_hash'], password):
        return user
    return None


def get_user_balance(user_id):
    """Получение баланса пользователя"""
    conn = get_db_connection()
    if not conn:
        return 0

    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE id = %s', (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0


def update_balance(user_id, amount, trans_type, description):
    """Обновление баланса и запись транзакции"""
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        # НЬЮ БАЛЕНС
        cursor.execute('''
        UPDATE users SET balance = balance + %s WHERE id = %s
        ''', (amount, user_id))

        # транз
        cursor.execute('''
        INSERT INTO transactions (user_id, type, cost, description)
        VALUES (%s, %s, %s, %s)
        ''', (user_id, trans_type, abs(amount), description))

        conn.commit()
        return True
    except Error as e:
        print(f"Ошибка обновления баланса: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_user_transactions(user_id, limit=10):
    """Получение истории транзакций"""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
    SELECT * FROM transactions 
    WHERE user_id = %s 
    ORDER BY id DESC 
    LIMIT %s
    ''', (user_id, limit))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return transactions