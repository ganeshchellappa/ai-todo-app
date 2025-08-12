import sqlite3
from contextlib import closing

DB_NAME = 'todo.db'

def init_db():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0
                )
            ''')

def get_all_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
    return [dict(task) for task in tasks]

def add_task(description):
    with sqlite3.connect(DB_NAME) as conn:
        with conn:
            conn.execute("INSERT INTO tasks (description, completed) VALUES (?, 0)", (description,))

def delete_task(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        with conn:
            conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))

def update_task_completion(task_id, completed):
    with sqlite3.connect(DB_NAME) as conn:
        with conn:
            conn.execute("UPDATE tasks SET completed=? WHERE id=?", (completed, task_id))

def update_task_description(task_id, description):
    with sqlite3.connect(DB_NAME) as conn:
        with conn:
            conn.execute("UPDATE tasks SET description=? WHERE id=?", (description, task_id))
