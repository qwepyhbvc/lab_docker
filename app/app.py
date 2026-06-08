from flask import Flask, request, render_template_string, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'task_db')
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
    <style>
        body { font-family: Arial; margin: 50px; }
        .container { max-width: 500px; margin: auto; }
        input, button { padding: 10px; margin: 5px; }
        ul { list-style: none; padding: 0; }
        li { padding: 10px; background: #f0f0f0; margin: 5px; }
        .delete { color: red; cursor: pointer; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Task Manager</h1>
        <form method="POST">
            <input type="text" name="task" placeholder="Enter task name" required>
            <button type="submit">Add Task</button>
        </form>
        <h2>Tasks:</h2>
        <ul>
            {% for task in tasks %}
            <li>{{ task[1] }} <a href="/delete/{{ task[0] }}" class="delete">Delete</a></li>
            {% else %}
            <li>No tasks yet</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
'''

def init_db():
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
    cursor.execute(f"USE {db_config['database']}")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        task_name = request.form.get('task', '').strip()
        if task_name:
            cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task_name,))
            conn.commit()
        return redirect(url_for('index'))
    cursor.execute("SELECT id, name FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
