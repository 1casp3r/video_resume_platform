# 📄 Resume AI Project

Это веб-приложение на FastAPI для анализа резюме (текстового и видео) с помощью AI.  
Также поддерживается система тестов и админка для их управления.

---

## 🚀 Быстрый старт

### 1. Клонирование проекта

```bash
git clone https://github.com/yourusername/resume-ai.git
cd resume-ai
```

### 2. Создание .env файла

Скопируй пример и укажи свои ключи:
```bash
cp .env.example .env
```

Открой `.env` и вставь значения:

```bash
# PostgreSQL
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db/resume_db

# Comet API
DOC_COMET_API_KEY=your_comet_api_key
DOC_COMET_API_URL=https://api.cometapi.com/v1/chat/completions

```

## 🔑 Где взять ключи?

### Comet API

- Зарегистрируйся: https://cometapi.com
- Перейди в настройки → API Keys
- Скопируй и вставь в .env

# 🐳 Запуск через Docker

### 1. Сборка контейнера
```bash
docker-compose build
```

### 2. Запуск проекта
```bash
docker-compose up
```

После запуска приложение будет доступно по адресу:
```bash
http://localhost:8000
```

# Функциональность

- Загрузка текстового резюме
- Загрузка видео и транскрипция
- AI-анализ содержания
- Система тестов с группами
- Админка для создания тестов