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
  - методы: create_note_title, create_note_content, view_note, edit_note, etc.
- Database
  - методы: create_note, get_notes, get_note, update_note, delete_note.
- Note
  - поля: id, user_id, title, content

---

### Доступные команды

`/start` - команда для старта бота

`/new` - создать новую заметку

`/list` - вывести все заметки

`/view` - вывести заметку по ID

`/edit` - редактировать заметку по ID

`/export` - экспортировать заметку в .txt по ID

`/delete` - удалить заметку по ID

---

### Зависимости

- sqlite3
- pyTelegramBotAPI
- python-dotenv

---

### Установка и запуск бота

```
git clone https://github.com/omgthatsjackie/mipt-python-creanote.git
cd mipt-python-creanote/
pip install -r requirements.txt
cd src/
python app.py
```
