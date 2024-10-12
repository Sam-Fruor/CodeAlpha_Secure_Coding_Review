from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    conn = sqlite3.connect('example.db')
    return conn

# Vulnerable login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vulnerable SQL query (SQL Injection)
        conn = get_db()
        cur = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cur.execute(query)
        user = cur.fetchone()

        if user:
            return f"Welcome {username}!"
        else:
            return "Invalid credentials."

    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# Vulnerable user profile route
@app.route('/profile/<username>')
def profile(username):
    # Vulnerable to XSS (Cross-Site Scripting)
    return render_template_string(f"<h1>Welcome, {username}</h1>")

if __name__ == "__main__":
    app.run(debug=True)
