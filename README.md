## Creanote

---

### Описание проекта

Телеграм-бот для создания заметок.

---

### Функционал

- позволяет создавать заметки, которые хранит в базе данных
- возможность экспортировать заметки в .txt формате
- возможность редактировать заметки

---

### Архитектура

Классы:

- Bot
  - методы: start, create_note, get_notes, delete_note, edit_note, update_note_title, update_note_content, export_notes, run, etc.
- Database
  - методы: create_note, get_notes, get_note_by_title, update_note, delete_note, close, etc.
- Note
  - поля: id, title, text, etc.

---

### Доступные команды

---

### Зависимости

- sqlite3
- python-telegram-bot

---

### Установка и запуск бота

```
git clone https://github.com/omgthatsjackie/mipt-python-creanote.git
cd mipt-python-creanote/
pip install -r requirements.txt
cd src/
python app.py
```
