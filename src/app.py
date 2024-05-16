from telebot import TeleBot
from model import Database
from os import getenv
from dotenv import load_dotenv


class Bot:
    def __init__(self, token, db_file):
        self.bot = TeleBot(token)
        self.db = Database(db_file)

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, 'Привет, меня зовут Creanote! Я помогаю создавать заметки!\n'
                                                   'Вот доступные команды:\n/new - создать заметку\n'
                                                   '/list - показать все заметки\n/view - просмотреть заметку по ID\n'
                                                   '/edit - отредактировать заметку по ID\n/export - экспортировать заметку по ID\n'
                                                   '/delete - удалить заметку по ID')

        @self.bot.message_handler(commands=['new'])
        def new_note(message):
            self.bot.send_message(message.chat.id, 'Введите название заметки:')
            self.bot.register_next_step_handler(message, self.create_note_title)

        @self.bot.message_handler(commands=['list'])
        def list_notes(message):
            notes = self.db.get_notes(message.from_user.id)
            if notes:
                notes = [f"{notes[i].id}. {notes[i].title}" for i in range(len(notes))]
                self.bot.send_message(message.chat.id, "\n".join(notes))
            else:
                self.bot.send_message(message.chat.id, "У вас нет заметок!")

        @self.bot.message_handler(commands=['view'])
        def view_note(message):
            self.bot.send_message(message.chat.id, 'Введите ID заметки:')
            self.bot.register_next_step_handler(message, self.view_note)

        @self.bot.message_handler(commands=['edit'])
        def edit_note(message):
            self.bot.send_message(message.chat.id, 'Введите ID заметки:')
            self.bot.register_next_step_handler(message, self.edit_note)

        @self.bot.message_handler(commands=['export'])
        def export_note(message):
            self.bot.send_message(message.chat.id, 'Введите ID заметки:')
            self.bot.register_next_step_handler(message, self.export_note)

        @self.bot.message_handler(commands=['delete'])
        def delete_note(message):
            self.bot.send_message(message.chat.id, 'Введите ID заметки:')
            self.bot.register_next_step_handler(message, self.delete_note)

    def create_note_title(self, message):
        title = message.text
        self.bot.send_message(message.chat.id, 'Введите текст заметки:')
        self.bot.register_next_step_handler(message, lambda msg: self.create_note_content(msg, title))

    def create_note_content(self, message, title):
        content = message.text
        note_id = self.db.create_note(message.from_user.id, title, content)
        self.bot.send_message(message.chat.id, f'Заметка создана с ID {note_id}!')

    def view_note(self, message):
        note_id = int(message.text)
        note = self.db.get_note(note_id)
        if note and note.user_id == message.from_user.id:
            self.bot.send_message(message.chat.id, f'{note.title}\n\n{note.content}')
        else:
            self.bot.send_message(message.chat.id, 'Заметка не найдена!')

    def edit_note(self, message):
        note_id = int(message.text)
        note = self.db.get_note(note_id)
        if note and note.user_id == message.from_user.id:
            self.bot.send_message(message.chat.id, 'Введите новое название:')
            self.bot.register_next_step_handler(message, lambda msg: self.edit_note_title(msg, note_id))
        else:
            self.bot.send_message(message.chat.id, 'Заметка не найдена!')

    def edit_note_title(self, message, note_id):
        title = message.text
        self.bot.send_message(message.chat.id, 'Введите новый текст:')
        self.bot.register_next_step_handler(message, lambda msg: self.edit_note_content(msg, note_id, title))

    def edit_note_content(self, message, note_id, title):
        content = message.text
        self.db.update_note(note_id, title, content)
        self.bot.send_message(message.chat.id, 'Заметка отредактирована!')

    def export_note(self, message):
        note_id = int(message.text)
        note = self.db.get_note(note_id)
        if note and note.user_id == message.from_user.id:
            with open(f'note_{note_id}.txt', 'w') as f:
                f.write(f'{note.title}\n\n{note.content}')
            with open(f'note_{note_id}.txt', 'r') as f:
                self.bot.send_document(message.chat.id, f)
        else:
            self.bot.send_message(message.chat.id, 'Заметка не найдена!')

    def delete_note(self, message):
        note_id = int(message.text)
        note = self.db.get_note(note_id)
        if note and note.user_id == message.from_user.id:
            self.db.delete_note(note_id)
            self.bot.send_message(message.chat.id, 'Заметка удалена!')
        else:
            self.bot.send_message(message.chat.id, 'Заметка не найдена!')

    def run(self):
        self.bot.infinity_polling()


if __name__ == '__main__':
    load_dotenv()
    bot = Bot(getenv("KEY"), "notes.db")
    bot.run()
