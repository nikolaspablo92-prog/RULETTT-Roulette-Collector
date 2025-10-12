# 👥 СОВМЕСТНАЯ РАБОТА В VISUAL STUDIO CODE

## 🎯 Настройка командной работы в VS Code

### 📋 ТРЕБОВАНИЯ ДЛЯ УЧАСТНИКОВ

- Visual Studio Code (последняя версия)
- Git установлен на компьютере
- Аккаунт GitHub
- Расширение Live Share (устанавливается автоматически)

---

## 🚀 СПОСОБЫ СОВМЕСТНОЙ РАБОТЫ

### 1️⃣ **Live Share** (РЕКОМЕНДУЕТСЯ - мгновенная совместная работа)

#### Для хоста (вас)

1. **Установить расширение**: `Live Share Extension Pack`
2. **Войти в GitHub**: Ctrl+Shift+P → "Live Share: Sign in"
3. **Начать сессию**: Ctrl+Shift+P → "Live Share: Start Collaboration Session"
4. **Поделиться ссылкой**: Скопировать ссылку и отправить команде

#### Для участников

1. **Получить ссылку** от хоста
2. **Открыть в браузере** или VS Code
3. **Войти в GitHub** (если потребуется)
4. **Начать совместную работу** ✅

**🔥 Возможности Live Share:**

- Редактирование кода в реальном времени ✅
- Совместная отладка ✅
- Общий терминал ✅
- Синхронизация курсора ✅
- Голосовой чат (при наличии расширения) ✅

---

### 2️⃣ **GitHub Codespaces** (облачная IDE)

#### Создание Codespace

1. Перейти на GitHub: <https://github.com/nikolaspablo92-prog/RULETTT-Roulette-Collector>
2. Нажать **Code** → **Codespaces** → **Create codespace on main**
3. Подождать загрузки (2-3 минуты)
4. VS Code откроется в браузере с полным проектом

#### Запуск системы в Codespaces

```bash
# Установка зависимостей
pip install flask flask-cors pandas aiohttp

# Запуск API сервера
python api_server.py &

# Запуск веб-сервера
cd webapp && python -m http.server 8080 &
```

**🌐 Автоматический проброс портов:** VS Code предложит сделать порты публичными

---

### 3️⃣ **Git Collaboration** (классический подход)

#### Клонирование репозитория

```bash
git clone https://github.com/nikolaspablo92-prog/RULETTT-Roulette-Collector.git
cd RULETTT-Roulette-Collector
```

#### Создание веток для участников

```bash
# Для каждого участника
git checkout -b feature/имя-участника
git push -u origin feature/имя-участника
```

#### Настройка Python окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ⚡ БЫСТРЫЙ СТАРТ ДЛЯ КОМАНДЫ

### 📝 **Отправьте участникам эту инструкцию:**

```
🎲 ПОДКЛЮЧЕНИЕ К ПРОЕКТУ RULETTT

1. Установите VS Code: https://code.visualstudio.com/
2. Установите расширение Live Share Extension Pack
3. Войдите в GitHub в VS Code (Ctrl+Shift+P → "Live Share: Sign in")
4. Дождитесь ссылки Live Share от администратора
5. Откройте ссылку и начинайте работать!

🔗 Репозиторий: https://github.com/nikolaspablo92-prog/RULETTT-Roulette-Collector
```

---

## 🛠 VS CODE НАСТРОЙКИ ДЛЯ КОМАНДЫ

### 📦 **Рекомендуемые расширения** (будут предложены автоматически)

- **Live Share Extension Pack** - совместная работа
- **Python** - поддержка Python
- **Pylance** - улучшенная поддержка Python
- **GitLens** - расширенные возможности Git
- **Bracket Pair Colorizer** - подсветка скобок
- **Auto Rename Tag** - автопереименование HTML тегов
- **Thunder Client** - тестирование API

### ⚙️ **Настройки workspace** (уже созданы)

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "git.autofetch": true,
    "liveShare.audio": true
}
```

---

## 📡 ЗАПУСК СИСТЕМЫ В КОМАНДЕ

### 🖥️ **Локальный запуск** (каждый участник)

```bash
# Активация окружения
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Запуск серверов
python api_server.py &
cd webapp && python -m http.server 8080
```

### 🌐 **Доступ к интерфейсам:**

- **Dashboard**: <http://localhost:8080/dashboard.html>
- **Mobile**: <http://localhost:8080/mobile.html>
- **Analytics**: <http://localhost:8080/advanced_analytics.html>
- **API**: <http://localhost:5000/api/health>

---

## 🎯 РАБОЧИЙ ПРОЦЕСС КОМАНДЫ

### 📊 **Роли в проекте:**

- **🔧 Backend Developer** - работа с `api_server.py`, база данных
- **🎨 Frontend Developer** - интерфейсы в папке `webapp/`
- **📈 Data Analyst** - анализ данных, консольный коллектор
- **🐛 QA Tester** - тестирование, документация
- **🏗️ DevOps** - развертывание, CI/CD

### 🔄 **Git workflow:**

1. **Главная ветка**: `main` (защищена)
2. **Рабочие ветки**: `feature/название-фичи`
3. **Pull Request** для каждого изменения
4. **Code Review** обязателен

### 💬 **Коммуникация:**

- **Live Share Chat** - во время сессий
- **GitHub Issues** - для задач и багов
- **GitHub Discussions** - для обсуждений
- **Communication интерфейс** - встроенный чат в системе

---

## 🚀 ГОТОВЫЕ КОМАНДЫ

### **Для администратора:**

```bash
# Создать Live Share сессию
Ctrl+Shift+P → "Live Share: Start Collaboration Session"

# Поделиться терминалом
Ctrl+Shift+P → "Live Share: Share Terminal"

# Запустить все сервисы
start_local_rulettt.bat
```

### **Для участников:**

```bash
# Подключиться к Live Share
# (используйте полученную ссылку)

# Клонировать проект
git clone https://github.com/nikolaspablo92-prog/RULETTT-Roulette-Collector.git

# Создать свою ветку
git checkout -b feature/мое-имя
```

---

## 🎉 **ГОТОВО К КОМАНДНОЙ РАБОТЕ!**

**Выберите способ совместной работы:**

- **Live Share** - для синхронной работы в реальном времени
- **Codespaces** - для облачной разработки без настройки
- **Git + Local** - для классической распределенной работы

*Система готова к совместной разработке в VS Code!* 🚀
