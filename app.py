from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        author TEXT,
        status TEXT
    )''')

    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return render_template("index.html", books=books)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']

        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("INSERT INTO books(name, author, status) VALUES (?, ?, ?)",
                  (name, author, "Available"))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template("add_book.html")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
