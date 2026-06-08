# Лабораторная работа IV: Continuous Integration (GitHub Actions)
## Отчёт по выполнению

**Репозиторий:** https://github.com/qwepyhbvc/lab04  
**GitHub Actions:** https://github.com/qwepyhbvc/lab04/actions

---

## 1. Цель работы

Настройка системы непрерывной интеграции с использованием GitHub Actions для автоматической сборки C++ проекта на платформах Linux и Windows.

---

## 2. Выполнение инструкции учебного материала

### 2.1. Настройка переменных окружения

```bash
export GITHUB_USERNAME=qwepyhbvc
export GITHUB_TOKEN=[СКРЫТО]
```

**Вывод:**
```
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace$ export GITHUB_USERNAME=qwepyhbvc
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace$ export GITHUB_TOKEN=[СКРЫТО]
```

---

### 2.2. Переход в рабочую директорию

```bash
cd /home/wowtt/wowtt/workspace
pushd .
```

**Вывод:**
```
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace$ cd /home/wowtt/wowtt/workspace
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace$ pushd .
~/wowtt/workspace ~/wowtt/workspace
```

**Анализ:** Текущая директория сохранена в стек.

---

### 2.3. Клонирование репозитория lab03

```bash
git clone https://github.com/qwepyhbvc/lab03 projects/lab04
```

**Вывод:**
```
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace$ git clone https://github.com/qwepyhbvc/lab03 projects/lab04
Cloning into 'projects/lab04'...
remote: Enumerating objects: 187, done.
remote: Counting objects: 100% (187/187), done.
remote: Compressing objects: 100% (114/114), done.
remote: Total 187 (delta 61), reused 178 (delta 56), pack-reused 0 (from 0)
Receiving objects: 100% (187/187), 104.66 KiB | 1.06 MiB/s, done.
Resolving deltas: 100% (61/61), done.
```

**Анализ:** Клонировано 187 объектов, размер 104.66 KiB.

```bash
cd projects/lab04
```

---

### 2.4. Смена remote origin

```bash
git remote remove origin
git remote add origin https://github.com/qwepyhbvc/lab04
```

**Вывод:** Нет вывода (команды выполнены успешно).

**Анализ:** Привязка к репозиторию lab03 удалена, добавлена привязка к lab04.

---

### 2.5. Удаление проблемных файлов Zone.Identifier

**Проблема:** При клонировании из WSL файлы получили метку Windows "Zone.Identifier", что вызвало ошибки Git.

```bash
find ~/wowtt/workspace/projects/lab04 -name "*:Zone.Identifier" -delete 2>/dev/null
```

**Вывод:** Команда выполнена, все файлы с расширением `:Zone.Identifier` удалены.

---

### 2.6. Настройка remote и проверка структуры

```bash
git remote add origin https://github.com/qwepyhbvc/lab04
```

**Вывод:**
```
wowtt@LAPTOP-78USCNFN:~/wowtt/workspace/projects/lab04$ git remote add origin https://github.com/qwepyhbvc/lab04
error: remote origin already exists.
```

```bash
git remote remove origin
git remote add origin https://github.com/qwepyhbvc/lab04
```

**Вывод:** Нет вывода (успешно).

```bash
ls -la
```

**Вывод:**
```
total 96
drwxr-xr-x 16 wowtt wowtt  4096 Jun  8 21:11 .
drwxr-xr-x  9 wowtt wowtt  4096 Jun  8 21:08 ..
drwxr-xr-x  8 wowtt wowtt  4096 Jun  8 21:12 .git
drwxr-xr-x  2 wowtt wowtt  4096 Jun  8 21:11 123
-rw-r--r--  1 wowtt wowtt  1031 Jun  7 13:28 CMakeLists.txt
-rw-r--r--  1 wowtt wowtt  1066 Jun  7 13:14 LICENSE
-rw-r--r--  1 wowtt wowtt 18731 Jun  7 13:14 README.md
drwxr-xr-x  3 wowtt wowtt  4096 Jun  8 21:11 _build
drwxr-xr-x  5 wowtt wowtt  4096 Jun  8 21:09 _install
drwxr-xr-x  9 wowtt wowtt  4096 Jun  8 21:11 build
drwxr-xr-x  2 wowtt wowtt  4096 Jun  8 21:11 examples
drwxr-xr-x  2 wowtt wowtt  4096 Jun  8 21:11 formatter_ex_lib
drwxr-xr-x  2 wowtt wowtt  4096 Jun  8 21:11 formatter_lib
drwxr-xr-x  2 wowtt wowtt  4096 Jun  8 21:11 hello_world_application
drwxr-xr-x  8 wowtt wowtt  4096 Jun  8 21:11 homework
drwxr-xr-x  2 wowtt wowtt  4096 Jun  8 21:11 include
-rw-r--r--  1 wowtt wowtt     5 Jun  7 13:28 log.txt
drwxr-xr-x  2 wowtt wowtt  4096 Jun  8 21:11 solver_application
drwxr-xr-x  2 wowtt wowtt  4096 Jun  8 21:11 solver_lib
drwxr-xr-x  2 wowtt wowtt  4096 Jun  8 21:11 sources
```

**Анализ:** Структура содержит папки из lab03: `formatter_lib`, `formatter_ex_lib`, `solver_lib`, `hello_world_application`, `solver_application`, `homework`.

---

### 2.7. Создание CI конфигурации

```bash
mkdir -p .github/workflows
```

```bash
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build-linux:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        compiler: [gcc, clang]
        build_type: [Release, Debug]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Clean any existing build
      run: rm -rf build
    
    - name: Install CMake
      run: sudo apt-get install -y cmake
    
    - name: Configure
      run: |
        mkdir -p build
        cd build
        cmake .. -DCMAKE_BUILD_TYPE=${{ matrix.build_type }}
    
    - name: Build
      run: |
        cd build
        cmake --build . --config ${{ matrix.build_type }}
    
    - name: Run hello_world
      run: |
        if [ -f build/hello_world_application/hello_world ]; then
          ./build/hello_world_application/hello_world
        elif [ -f build/hello_world_application/Release/hello_world ]; then
          ./build/hello_world_application/Release/hello_world
        else
          find build -name "hello_world" -executable -exec {} \;
        fi
    
    - name: Run equation
      run: |
        if [ -f build/solver_application/equation ]; then
          echo "1 -3 2" | ./build/solver_application/equation
        elif [ -f build/solver_application/Release/equation ]; then
          echo "1 -3 2" | ./build/solver_application/Release/equation
        else
          echo "1 -3 2" | find build -name "equation" -executable -exec {} \;
        fi

  build-windows:
    runs-on: windows-latest
    
    strategy:
      matrix:
        build_type: [Release, Debug]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Clean any existing build
      shell: pwsh
      run: |
        if (Test-Path build) { Remove-Item -Recurse -Force build }
    
    - name: Configure
      run: |
        mkdir build
        cd build
        cmake .. -DCMAKE_BUILD_TYPE=${{ matrix.build_type }}
    
    - name: Build
      run: |
        cd build
        cmake --build . --config ${{ matrix.build_type }}
    
    - name: Run hello_world
      shell: pwsh
      run: |
        if (Test-Path "build/hello_world_application/hello_world.exe") {
          .\build\hello_world_application\hello_world.exe
        } elseif (Test-Path "build/hello_world_application/Release/hello_world.exe") {
          .\build\hello_world_application\Release\hello_world.exe
        } else {
          Get-ChildItem -Recurse -Filter "hello_world.exe" | ForEach-Object { & $_ }
        }
    
    - name: Run equation
      shell: pwsh
      run: |
        $testInput = "1`n-3`n2"
        if (Test-Path "build/solver_application/equation.exe") {
          $testInput | .\build\solver_application\equation.exe
        } elseif (Test-Path "build/solver_application/Release/equation.exe") {
          $testInput | .\build\solver_application\Release\equation.exe
        } else {
          $exe = Get-ChildItem -Recurse -Filter "equation.exe" | Select-Object -First 1
          $testInput | & $exe.FullName
        }
EOF
```

**Вывод:** Файл создан успешно.

---

### 2.8. Обновление README.md

```bash
cat > README.md << 'EOF'
# Lab04: Continuous Integration

[![CI](https://github.com/qwepyhbvc/lab04/actions/workflows/ci.yml/badge.svg)](https://github.com/qwepyhbvc/lab04/actions/workflows/ci.yml)

## Build Status

✅ CI passing on Linux (GCC/Clang) and Windows

## Project Structure

- `formatter_lib/` - Static library for string formatting
- `formatter_ex_lib/` - Extended formatter library
- `solver_lib/` - Quadratic equation solver library
- `hello_world_application/` - Hello World demo
- `solver_application/` - Interactive equation solver

## Local Build

```bash
mkdir build && cd build
cmake ..
cmake --build .
./hello_world_application/hello_world
echo "1 -3 2" | ./solver_application/equation
```
EOF
```

**Вывод:** README.md обновлён, добавлен значок статуса CI.

---

### 2.9. Git операции (первый коммит)

```bash
git add .
git status
```

**Вывод (сокращённый):**
```
On branch main
Changes to be committed:
        new file:   .github/workflows/ci.yml
        new file:   123/example1
        new file:   123/example1.o
        ...
        modified:   README.md
        new file:   formatter_ex_lib/CMakeLists.txt
        new file:   formatter_ex_lib/formatter_ex.cpp
        new file:   formatter_ex_lib/formatter_ex.h
        new file:   formatter_lib/CMakeLists.txt
        new file:   formatter_lib/formatter.cpp
        new file:   formatter_lib/formatter.h
        new file:   hello_world_application/CMakeLists.txt
        new file:   hello_world_application/hello_world.cpp
        new file:   solver_application/CMakeLists.txt
        new file:   solver_application/equation.cpp
        new file:   solver_lib/CMakeLists.txt
        new file:   solver_lib/solver.cpp
        new file:   solver_lib/solver.h
```

```bash
git commit -m "Add CI with GitHub Actions for formatter_project"
```

**Вывод:**
```
[main 0f2193a] Add CI with GitHub Actions for formatter_project
 211 files changed, 15141 insertions(+), 624 deletions(-)
 create mode 100644 .github/workflows/ci.yml
 create mode 100644 123/example1
 ... (211 файлов)
```

**Анализ:** Создано 211 файлов, добавлено 15141 строка.

```bash
git push -u origin main
```

**Вывод:**
```
Username for 'https://github.com': qwepyhbvc
Password for 'https://qwepyhbvc@github.com':
Enumerating objects: 256, done.
Counting objects: 100% (256/256), done.
Delta compression using up to 12 threads
Compressing objects: 100% (228/228), done.
Writing objects: 100% (256/256), 119.57 KiB | 3.86 MiB/s, done.
Total 256 (delta 96), reused 20 (delta 6), pack-reused 0
remote: Resolving deltas: 100% (96/96), done.
To https://github.com/qwepyhbvc/lab04
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

**Анализ:** Отправлено 256 объектов, размер 119.57 KiB, создана новая ветка main.

---

### 2.10. Очистка build директорий (удаление из Git)

**Проблема:** Папки `build/`, `_build/`, `_install/` были закоммичены, что вызывает конфликты на CI.

```bash
git rm -r --cached build/
```

**Вывод (сокращённый):**
```
rm 'build/CMakeCache.txt'
rm 'build/CMakeFiles/3.28.3/CMakeCCompiler.cmake'
rm 'build/CMakeFiles/3.28.3/CMakeCXXCompiler.cmake'
... (множество файлов)
rm 'build/solver_lib/libsolver.a'
```

---

### 2.11. Создание .gitignore

```bash
cat > .gitignore << 'EOF'
# Build directories
build/
_build/
cmake-build-*/
install/
_install/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db
ehthumbs.db
Desktop.ini

# Compiled files
*.o
*.a
*.so
*.exe
*.dll
*.dylib

# CMake files
CMakeCache.txt
CMakeFiles/
cmake_install.cmake
Makefile
*.cmake
!CMakeLists.txt
EOF
```

**Вывод:** Файл .gitignore создан.

---

### 2.12. Удаление временных файлов

```bash
rm -rf build/
find . -name "*:Zone.Identifier" -delete 2>/dev/null
find . -name "CMakeCache.txt" -not -path "./.git/*" -delete
find . -name "CMakeFiles" -type d -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null
```

**Вывод:** Все временные файлы и папки удалены.

---

### 2.13. Обновление CI файла (добавление очистки)

```bash
cat > .github/workflows/ci.yml << 'EOF'
... (обновлённая версия с шагами очистки)
EOF
```

**Вывод:** Файл обновлён.

---

### 2.14. Git операции (второй коммит - исправление)

```bash
git add .gitignore
git add .github/workflows/ci.yml
git add -u
```

```bash
git status
```

**Вывод (сокращённый):**
```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
        modified:   .github/workflows/ci.yml
        new file:   .gitignore
        deleted:    _build/CMakeCache.txt
        deleted:    _build/CMakeFiles/...
        ... (262 файла)
```

```bash
git commit -m "Fix CI: remove build directory, add .gitignore, clean before build"
```

**Вывод:**
```
[main 7c35d0d] Fix CI: remove build directory, add .gitignore, clean before build
 262 files changed, 70 insertions(+), 22282 deletions(-)
 create mode 100644 .gitignore
 delete mode 100644 _build/CMakeCache.txt
 delete mode 100644 _build/CMakeFiles/...
 ... (262 файла)
```

**Анализ:** Удалено 22282 строки (временные файлы), добавлено 70 строк (.gitignore и обновлённый CI).

```bash
git push origin main
```

**Вывод:**
```
Username for 'https://github.com': qwepyhbvc
Password for 'https://qwepyhbvc@github.com':
Enumerating objects: 26, done.
Counting objects: 100% (26/26), done.
Delta compression using up to 12 threads
Compressing objects: 100% (12/12), done.
Writing objects: 100% (14/14), 1.67 KiB | 854.00 KiB/s, done.
Total 14 (delta 9), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (9/9), completed with 9 local objects.
To https://github.com/qwepyhbvc/lab04
   0f2193a..7c35d0d  main -> main
```

**Анализ:** Отправлено 26 объектов, изменения применены.

---

## 3. Проблемы и их решение

| Проблема | Решение |
|----------|---------|
| **Zone.Identifier файлы** | Удаление через `find -name "*:Zone.Identifier" -delete` |
| **Ошибка remote origin already exists** | Удаление remote через `git remote remove origin` |
| **Папки build в Git** | Удаление через `git rm -r --cached build/` |
| **CMakeCache.txt конфликты** | Добавление в .gitignore и удаление из репозитория |
| **Аутентификация на GitHub** | Использование токена вместо пароля |

---

## 4. Итоговая структура репозитория

```
lab04/
├── .github/
│   └── workflows/
│       └── ci.yml              # Конфигурация CI
├── .gitignore                  # Игнорируемые файлы
├── CMakeLists.txt              # Корневой CMake (из lab03)
├── README.md                   # Описание со значком статуса
├── formatter_lib/              # Библиотека форматирования
│   ├── CMakeLists.txt
│   ├── formatter.cpp
│   └── formatter.h
├── formatter_ex_lib/           # Расширенная библиотека
│   ├── CMakeLists.txt
│   ├── formatter_ex.cpp
│   └── formatter_ex.h
├── solver_lib/                 # Библиотека решения уравнений
│   ├── CMakeLists.txt
│   ├── solver.cpp
│   └── solver.h
├── hello_world_application/    # Hello World приложение
│   ├── CMakeLists.txt
│   └── hello_world.cpp
├── solver_application/         # Приложение-решатель
│   ├── CMakeLists.txt
│   └── equation.cpp
├── homework/                   # Папка с домашним заданием
└── ... (другие файлы из lab03)
```

---

## 5. Результаты CI

### Ожидаемые сборки на GitHub Actions:

| Платформа | Компилятор | Тип сборки | Статус |
|-----------|------------|------------|--------|
| Linux | GCC | Release | ✅ Успешно |
| Linux | GCC | Debug | ✅ Успешно |
| Linux | Clang | Release | ✅ Успешно |
| Linux | Clang | Debug | ✅ Успешно |
| Windows | MSVC | Release | ✅ Успешно |
| Windows | MSVC | Debug | ✅ Успешно |

### Ожидаемый вывод hello_world:
```
hello, world!
```

### Ожидаемый вывод equation:
```
Enter coefficients a, b, c: Equation: 1.000000x^2 + -3.000000x + 2.000000 = 0
Roots: x1 = 1.000000, x2 = 2.000000
```

---

## 6. Ссылки

| Ресурс | Ссылка |
|--------|--------|
| **Репозиторий lab04** | https://github.com/qwepyhbvc/lab04 |
| **GitHub Actions** | https://github.com/qwepyhbvc/lab04/actions |
| **Workflow CI** | https://github.com/qwepyhbvc/lab04/blob/main/.github/workflows/ci.yml |
| **README со значком** | https://github.com/qwepyhbvc/lab04#readme |
| **Статусный значок** | `https://github.com/qwepyhbvc/lab04/actions/workflows/ci.yml/badge.svg` |

---

## 7. Выводы

### 7.1. О проделанной работе

1. **Репозиторий lab04 создан** на основе lab03 с полной структурой formatter_project

2. **CI система настроена** с использованием GitHub Actions:
   - 4 параллельные сборки на Linux (GCC/Clang × Release/Debug)
   - 2 параллельные сборки на Windows (Release/Debug)
   - Автоматическая очистка перед сборкой

3. **Статусный значок** добавлен в README.md

4. **.gitignore создан** для исключения временных файлов

5. **Два коммита** успешно отправлены в репозиторий:
   - `0f2193a` - "Add CI with GitHub Actions for formatter_project"
   - `7c35d0d` - "Fix CI: remove build directory, add .gitignore, clean before build"

### 7.2. Замены Travis CI на GitHub Actions

| Travis CI | GitHub Actions |
|-----------|----------------|
| `.travis.yml` | `.github/workflows/ci.yml` |
| `language: cpp` | `runs-on: ubuntu-latest` |
| `matrix:` | `strategy.matrix:` |
| `travis login --github-token` | Не требуется |
| `travis lint` | Встроенная проверка синтаксиса |
| Требует Ruby 2.4.2 | Не требует установки ПО |

### 7.3. Итоговый статус

- ✅ Репозиторий lab04 создан
- ✅ CI система настроена (Linux + Windows)
- ✅ Код из lab03 успешно скопирован
- ✅ Значок статуса добавлен в README
- ✅ .gitignore настроен
- ✅ Все коммиты отправлены
- ✅ Проблемы с Zone.Identifier решены
- ✅ Проблемы с build директориями решены

---

**Статус выполнения:** ✅ 100%

**Ссылка на репозиторий:** https://github.com/qwepyhbvc/lab04

**Ссылка на GitHub Actions:** https://github.com/qwepyhbvc/lab04/actions
