from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import *
import hashlib

app = Flask(__name__)
app.secret_key = 'secretkey123'

# Создаем бд
init_db()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login', '').strip()
        password = request.form.get('password', '')

        user = authenticate_user(login, password)  

        if user:
            session['user_id'] = user['id']
            session['login']   = user['username']
            session['name']    = user.get('surname') or user['username']
            flash('Вход выполнен!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный логин или пароль', 'danger')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    balance = get_user_balance(session['user_id'])
    transactions = get_user_transactions(session['user_id'])

    return render_template('dashboard.html',
                           name=session['name'],
                           balance=balance,
                           transactions=transactions)


@app.route('/buy', methods=['POST'])
def buy():
    amount = int(request.form['amount'])
    balance = get_user_balance(session['user_id'])

    if amount > balance:
        flash('Ноумани', 'danger')
    else:
        update_balance(session['user_id'], -amount, 'purchase', f'Покупка на {amount} монет')
        flash(f'Куплено на {amount} бачей!', 'success')

    return redirect(url_for('dashboard'))


@app.route('/add-funds', methods=['POST'])
def add_funds():
    amount = int(request.form['amount'])

    if amount > 0:
        update_balance(session['user_id'], amount, 'deposit', f'Пополнение на {amount} монет')
        flash(f'Баланс пополнен на {amount} монет!', 'success')

    return redirect(url_for('dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('login', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')
        surname  = request.form.get('surname', '').strip()
        lastname = request.form.get('lastname', '').strip() or None

        if not username or not email or not password or not surname:
            flash('Заполните все обязательные поля', 'danger')
            return render_template('register.html')

        if password != confirm:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html')

        user_id = add_user(
            username=username,
            email=email,
            password=password,
            surname=surname,
            lastname=lastname,
        )

        if user_id:
            flash('Регистрация успешна, войдите', 'success')
            return redirect(url_for('login'))
        else:
            flash('Логин или email уже заняты', 'danger')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)