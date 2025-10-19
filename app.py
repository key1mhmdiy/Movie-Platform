# server/app.py
from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "movies.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                poster TEXT NOT NULL,
                url TEXT NOT NULL,
                genre TEXT,
                year INTEGER,
                description TEXT
            )
        ''')
        # فیلم نمونه
        cursor.execute('''
            INSERT INTO movies (title, poster, url, genre, year, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            "دکتر استرنج: دنیای دیوانگی چندجهانی",
            "https://m.media-amazon.com/images/M/MV5BNWM0ZGJlMzMtZmYwMi00NzI3LTgzMzMtNjMzNjliNDRmZmFlXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_.jpg",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
            "اکشن",
            2022,
            "دکتر استرنج وارد دنیای دیوانگی چندجهانی می‌شود..."
        ))
        conn.commit()
        conn.close()

@app.route('/api/movies')
def get_movies():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies ORDER BY year DESC")
        movies = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    print("🚀 سرور API در حال اجراست: http://localhost:5000/api/movies")
    app.run(debug=True, host='0.0.0.0', port=5000)