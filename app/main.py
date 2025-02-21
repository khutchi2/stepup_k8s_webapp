from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')

# Replace before_first_request with init-db CLI command
@app.cli.command('init-db')
def init_db_command():
    """Initialize the database."""
    init_db()
    print('Initialized the database.')

# Move database check to a before_request handler
@app.before_request
def check_database():
    if not os.path.exists(DATABASE):
        init_db()

@app.route('/api/items', methods=['GET'])
def get_items():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        return jsonify([{'id': item[0], 'name': item[1], 'description': item[2]} for item in items])

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
        
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)',
                      (data['name'], data.get('description', '')))
        conn.commit()
        return jsonify({'id': cursor.lastrowid}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)