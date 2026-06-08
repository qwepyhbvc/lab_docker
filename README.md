# Лабораторная работа: Docker

## Отчёт по выполнению

**Репозиторий:** https://github.com/qwepyhbvc/lab_docker

---

## Часть 1: Основное задание (Tutorial)

### 1.1. Настройка переменных окружения

```bash
export GITHUB_USERNAME=qwepyhbvc
export GIST_TOKEN=ghp_<TOKEN>
alias edit=nano
```

**Вывод:**
```
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace/projects$ export GITHUB_USERNAME=qwepyhbvc
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace/projects$ export GIST_TOKEN=ghp_<TOKEN>
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace/projects$ alias edit=nano
```

---

### 1.2. Создание репозитория lab_docker

```bash
git clone https://github.com/${GITHUB_USERNAME}/lab06 projects/lab_docker
cd projects/lab_docker
git remote remove origin
git remote add origin https://github.com/${GITHUB_USERNAME}/lab_docker
git remote -v
```

**Вывод:**
```
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace/projects$ git clone https://github.com/qwepyhbvc/lab06 projects/lab_docker
Cloning into 'projects/lab_docker'...
remote: Enumerating objects: 370, done.
remote: Counting objects: 100% (370/370), done.
remote: Compressing objects: 100% (199/199), done.
remote: Total 370 (delta 148), reused 352 (delta 134), pack-reused 0 (from 0)
Receiving objects: 100% (370/370), 159.59 KiB | 1.70 MiB/s, done.
Resolving deltas: 100% (148/148), done.

wowtt@LAPTOP-78USCNFN:~/wowtt/workspace/projects$ cd projects/lab_docker
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace/projects/projects/lab_docker$ git remote remove origin
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace/projects/projects/lab_docker$ git remote add origin https://github.com/qwepyhbvc/lab_docker
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace/projects/projects/lab_docker$ git remote -v
origin  https://github.com/qwepyhbvc/lab_docker (fetch)
origin  https://github.com/qwepyhbvc/lab_docker (push)
```

---

### 1.3. Установка Docker

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

**Вывод (фрагменты):**
```
Get:1 https://download.docker.com/linux/ubuntu noble InRelease [48.5 kB]
Get:2 https://download.docker.com/linux/ubuntu noble/stable amd64 Packages [56.9 kB]
...
Setting up docker-ce (5:29.5.3-1~ubuntu.24.04~noble) ...
Docker version 29.5.3, build d1c06ef
Docker Compose version v5.1.4
```

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

**Вывод:**
```
Synchronizing state of docker.service with SysV service script with /usr/lib/systemd/systemd-sysv-install.
Executing: /usr/lib/systemd/systemd-sysv-install enable docker
```

---

### 1.4. Создание простого Python приложения

```bash
cat > main.py << 'EOF'
print("Hello, Docker!")
EOF
```

```bash
cat > requirements.txt << 'EOF'
flask
requests
EOF
```

**Вывод:** Файлы `main.py` и `requirements.txt` созданы.

---

### 1.5. Создание Dockerfile

```bash
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
EOF
```

**Вывод:** Файл `Dockerfile` создан.

---

### 1.6. Сборка и запуск Docker образа

```bash
docker build -t lab-docker .
```

**Вывод:**
```
[+] Building 251.9s (11/11) FINISHED
 => [1/6] FROM docker.io/library/python:3.9-slim
 => [2/6] WORKDIR /app
 => [3/6] RUN apt-get update && apt-get install -y build-essential
 => [4/6] COPY requirements.txt .
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt
 => [6/6] COPY . .
 => exporting to image
 => => naming to docker.io/library/lab-docker:latest
```

```bash
docker run --rm -it lab-docker
```

**Вывод:**
```
Hello, Docker!
```

---

### 1.7. Создание docker-compose.yml

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  app:
    build: . 
    container_name: lab_docker
    environment:
      - DB_HOST=$DB_HOST
      - DB_USER=$DB_USER
      - DB_PASSWORD=$DB_PASSWORD
      - DB_NAME=$DB_NAME

  db:
    image: mysql:8.0
    container_name: mysql_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: $DB_ROOT_PASSWORD
      MYSQL_DATABASE: $DB_NAME
      MYSQL_USER: $DB_USER
      MYSQL_PASSWORD: $DB_PASSWORD
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db_data:
EOF
```

---

### 1.8. Создание .env файла

```bash
cat > .env << 'EOF'
DB_HOST=db
DB_USER=app_user
DB_PASSWORD=app_password
DB_NAME=app_db
DB_ROOT_PASSWORD=root_password
EOF
```

---

### 1.9. Git операции (основное задание)

```bash
git add .
git commit -m "Add Docker configuration"
git push origin main
```

**Вывод:**
```
[main d7f8dc6] Add Docker configuration
 4 files changed, 53 insertions(+)
 create mode 100644 .env
 create mode 100644 Dockerfile
 create mode 100644 docker-compose.yml
 create mode 100644 main.py
To https://github.com/qwepyhbvc/lab_docker
 * [new branch]      main -> main
```

---

## Часть 2: Домашнее задание

### Формулировка ДЗ:

> В репозитории приведен код web-приложения, которое сохраняет в БД введенную информацию о задаче - ее имя.

### 2.1. Пункт ДЗ №1: Создание web-приложения

```bash
mkdir -p app db
```

```bash
cat > app/app.py << 'EOF'
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
EOF
```

---

### 2.2. Пункт ДЗ №2: Создание requirements.txt

```bash
cat > app/requirements.txt << 'EOF'
flask==2.3.3
mysql-connector-python==8.1.0
EOF
```

---

### 2.3. Пункт ДЗ №3: Создание SQL инициализации

```bash
cat > db/init.sql << 'EOF'
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO tasks (name) VALUES ('Example task');
EOF
```

---

### 2.4. Пункт ДЗ №4: Обновление Dockerfile

```bash
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
EOF
```

---

### 2.5. Пункт ДЗ №5: Обновление docker-compose.yml

```bash
cat > docker-compose.yml << 'EOF'
services:
  web:
    build: .
    container_name: task_manager_web
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_USER=task_user
      - DB_PASSWORD=task_password
      - DB_NAME=task_db
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: mysql:8.0
    container_name: task_manager_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: task_db
      MYSQL_USER: task_user
      MYSQL_PASSWORD: task_password
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-proot_password"]
      interval: 10s
      timeout: 5s
      retries: 10

volumes:
  db_data:
EOF
```

---

### 2.6. Пункт ДЗ №6: Запуск связки web-приложение + БД

```bash
docker compose up --build -d
```

**Вывод:**
```
[+] Building 146.0s (13/13) FINISHED
 => [3/6] RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt
 => [6/6] COPY app/ .
 => exporting to image
[+] up 19/19
 ✔ Image mysql:8.0            Pulled
 ✔ Image lab_docker-web       Built
 ✔ Container task_manager_db  Healthy
 ✔ Container task_manager_web Started
```

---

### 2.7. Пункт ДЗ №7: Проверка статуса контейнеров

```bash
docker ps
```

**Вывод:**
```
CONTAINER ID   IMAGE            COMMAND                  STATUS                    PORTS
18a0c10fa780   lab_docker-web   "python app.py"          Up Less than a second     0.0.0.0:5000->5000/tcp
fba4e45dfbc1   mysql:8.0        "docker-entrypoint.s…"   Up 28 seconds (healthy)   0.0.0.0:3306->3306/tcp
```

---

### 2.8. Пункт ДЗ №8: Проверка работы приложения через curl

```bash
curl http://localhost:5000
```

**Вывод:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
    ...
            <li>Example task <a href="/delete/1" class="delete">Delete</a></li>
    ...
</html>
```

**Анализ:** Приложение работает, база данных содержит тестовую задачу "Example task".

---

### 2.9. Пункт ДЗ №9: Просмотр логов

```bash
docker compose logs web
```

**Вывод:**
```
task_manager_web  |  * Serving Flask app 'app'
task_manager_web  |  * Debug mode: on
task_manager_web  |  * Running on all addresses (0.0.0.0)
task_manager_web  |  * Running on http://127.0.0.1:5000
task_manager_web  |  * Running on http://172.18.0.3:5000
task_manager_web  |  * Debugger PIN: 104-641-688
```

---

### 2.10. Пункт ДЗ №10: Остановка контейнеров

```bash
docker compose down
```

**Вывод:**
```
[+] down 3/3
 ✔ Container task_manager_web Removed
 ✔ Container task_manager_db  Removed
 ✔ Network lab_docker_default Removed
```

---

### 2.11. Пункт ДЗ №11: Git операции (финальный коммит)

```bash
git add .
git commit -m "Complete Docker lab with web application"
git push origin main
```

**Вывод:**
```
[main 3c9d120] Complete Docker lab with web application
 4 files changed, 133 insertions(+), 19 deletions(-)
 create mode 100644 app/app.py
 create mode 100644 db/init.sql
To https://github.com/qwepyhbvc/lab_docker
   d7f8dc6..3c9d120  main -> main
```

---

## Часть 3: Результаты выполнения

### 3.1. Основное задание (Tutorial)

| Пункт | Выполнено |
|-------|-----------|
| Установка Docker | ✅ |
| Создание простого Python приложения | ✅ |
| Создание Dockerfile | ✅ |
| Сборка Docker образа | ✅ |
| Запуск контейнера | ✅ |
| Создание docker-compose.yml | ✅ |
| Запуск через Docker Compose | ✅ |

### 3.2. Домашнее задание (Homework)

| Пункт ДЗ | Описание | Статус |
|----------|----------|--------|
| **Пункт 1** | Создание web-приложения на Flask | ✅ |
| **Пункт 2** | Создание requirements.txt | ✅ |
| **Пункт 3** | Создание SQL инициализации БД | ✅ |
| **Пункт 4** | Обновление Dockerfile для web-приложения | ✅ |
| **Пункт 5** | Обновление docker-compose.yml с MySQL | ✅ |
| **Пункт 6** | Запуск связки web-приложение + БД | ✅ |
| **Пункт 7** | Проверка статуса контейнеров | ✅ |
| **Пункт 8** | Проверка работы приложения (curl) | ✅ |
| **Пункт 9** | Просмотр логов | ✅ |
| **Пункт 10** | Остановка контейнеров | ✅ |
| **Пункт 11** | Отправка в Git | ✅ |

---

## Часть 4: Структура репозитория

```
lab_docker/
├── app/
│   ├── app.py
│   └── requirements.txt
├── db/
│   └── init.sql
├── Dockerfile
├── docker-compose.yml
├── .env
├── main.py
├── requirements.txt
└── README.md
```

---

## Часть 5: Скриншоты

### Скриншот работы приложения в браузере

При открытии `http://localhost:5000` отображается:
- Заголовок "Task Manager"
- Поле ввода для новой задачи
- Кнопка "Add Task"
- Список задач с кнопкой "Delete"
- Тестовая задача "Example task"

скриншот 1. (добавление Example task, 123, фыв, 8 лаба, qwe, asd, докер)
![+ Example task, 123, фыв, 8 лаба, qwe, asd, докер](https://github.com/qwepyhbvc/lab_docker/blob/main/123/%D0%B8%D1%81%D1%85%D0%BE%D0%B4.jpg)

скриншот 2. (убираем докер)
![- докер](https://github.com/qwepyhbvc/lab_docker/blob/main/123/-%D0%B4%D0%BE%D0%BA%D0%B5%D1%80.jpg)

скриншот 3. (убираем всё, кроме Example task, добавляем zxc, докер2)
![- 123, фыв, 8 лаба, qwe, asd, докер | + zxc, докер2](https://github.com/qwepyhbvc/lab_docker/blob/main/123/-%20%D0%B2%D1%81%D1%91%20%2B%20%D0%B4%D0%BE%D0%BA%D0%B5%D1%802%20%2B%20zxc%20(%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80%20%D0%B1%D0%B5%D0%B7%20%D0%B8%D0%B7%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8%D0%B9).jpg)
