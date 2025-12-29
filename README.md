# avito-qa-internship

Python 3.12+

# Структура проекта
.
├── .venv/               # Папка виртуального окружения
├── test_api.py          # Файл с автотестами
├── BUGS.md              # Отчет о найденных дефектах
├── README.md            # Данный файл с инструкцией
├── TESTCASES.md         # Описание тест-кейсов в табличном виде
└── requirements.txt     # Список зависимостей проекта

# 1. Клонируйте репозиторий
## Для Windows:
bash python -m venv venv venv\Scripts\activate

## Для macOS / Linux:
bash python3 -m venv venv source venv/bin/activate


# 2. Установите зависимости

pip install -r requirements.txt


# 3. Запустите тесты

pytest -v

