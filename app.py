from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management!

# -------- ROUTES --------
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        # Add placeholders for other fields
        first_name = ''
        last_name = ''
        date_of_birth = ''

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("""
                INSERT INTO users 
                (username, email, password, first_name, last_name, date_of_birth) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, email, hashed_pw, first_name, last_name, date_of_birth))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered. Please use a different email."
        conn.close()

        session['user'] = username
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            return redirect(url_for('home'))
        else:
            return "Login failed. Invalid email or password."

    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['user'])

@app.route('/mood')
def mood():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('mood.html')

@app.route('/detect')
def detect():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('detect.html')

# -------- MAIN --------
if __name__ == '__main__':
    app.run(debug=True)