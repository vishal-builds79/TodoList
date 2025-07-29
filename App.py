from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, done INTEGER DEFAULT 0)')

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    return redirect('/')

@app.route('/done/<int:id>')
def done(id):
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('UPDATE tasks SET done = 1 WHERE id=?', (id,))
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('DELETE FROM tasks WHERE id=?', (id,))
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)