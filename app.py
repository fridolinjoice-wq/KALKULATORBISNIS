from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# DATABASE
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cashflow (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pendapatan REAL,
            pengeluaran REAL,
            hasil REAL,
            status TEXT,
            waktu TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None
    status = None

    if request.method == "POST":
        pendapatan = float(request.form["pendapatan"])
        pengeluaran = float(request.form["pengeluaran"])

        hasil = pendapatan - pengeluaran

        if hasil > 0:
            status = "surplus"
        elif hasil < 0:
            status = "defisit"
        else:
            status = "imbang"

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO cashflow (pendapatan, pengeluaran, hasil, status, waktu)
            VALUES (?, ?, ?, ?, ?)
        """, (pendapatan, pengeluaran, hasil, status, datetime.now()))
        conn.commit()
        conn.close()

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM cashflow ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    return render_template("index.html", hasil=hasil, status=status, data=data)


# 🔥 RESET TOTAL DATABASE
@app.route("/reset")
def reset():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM cashflow")
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)