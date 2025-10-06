from flask import Flask, render_template, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- создаём таблицу, если её нет ---
def init_db():
    with sqlite3.connect("support.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS support_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            message TEXT
        )
        """)
init_db()

# --- главная страница ---
@app.route('/')
def index():
    return render_template('index.html')

# --- страница админки ---
@app.route('/admin')
def admin():
    return render_template('admin.html')

# --- API: отправка сообщения ---
@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data['username']
    email = data['email']
    message = data['message']

    with sqlite3.connect("support.db") as conn:
        conn.execute("INSERT INTO support_messages (username, email, message) VALUES (?, ?, ?)",
                     (username, email, message))
    return jsonify({"status": "ok"})

# --- API: получение всех сообщений ---
@app.route('/api/messages', methods=['GET'])
def get_messages():
    with sqlite3.connect("support.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM support_messages")
        data = cur.fetchall()
    return jsonify(data)

# --- API: удаление сообщения ---
@app.route('/api/delete/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    with sqlite3.connect("support.db") as conn:
        conn.execute("DELETE FROM support_messages WHERE id=?", (msg_id,))
    return jsonify({"status": "deleted"})

if __name__ == '__main__':
    app.run(debug=True)
