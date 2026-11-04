from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Database connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)


# Add task
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")

    if title and title.strip():
        conn = get_db_connection()

        conn.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description)
        )

        conn.commit()
        conn.close()

    return redirect(url_for("home"))


# Complete task
@app.route("/complete/<int:id>")
def complete_task(id):
    conn = get_db_connection()

    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


# Delete task
@app.route("/delete/<int:id>")
def delete_task(id):
    conn = get_db_connection()

    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


# About page
@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
