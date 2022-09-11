import config
import sqlite3
import datetime
from xlsxwriter.workbook import Workbook

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.name_db = db_file
        self.session_date = datetime.datetime.now(tz=config.tz).date()

    def user_exists(self, user_id):
        """Проверяем, есть ли пользователь БД True/False"""
        result = self.cursor.execute("SELECT `id` FROM `user` WHERE `telegram_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def new_row_user(self, telegram_id, username, date, thing, brend, model, size, factors, telephone):
        """Добавляем новый заказ в таблицу user"""
        self.cursor.execute("INSERT INTO `user` (`telegram_id`, `username`, `date`, `thing`, `brend`, `model`, `size`, `factors`, `telephone`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (telegram_id, username, date, thing, brend, model, size, factors, telephone))
        return self.conn.commit()

    # def update_in_user(self, user_id, dict_values):
    #     """ Изменяет значения в user по id; принимает словарь """
    #     for i in dict_values:
    #         self.cursor.execute(f'UPDATE user SET {i} = ? WHERE telegram_id = ?',
    #                             (dict_values[i], user_id, ))
    #     return self.conn.commit()

    def backup(self):
        backup_con = sqlite3.connect('backup.db')
        try:
            with backup_con:
                self.conn.backup(backup_con, pages=3)
            mess = True
        except sqlite3.Error as error:
            mess = error
        finally:
            if (backup_con):
                backup_con.close()
        return mess

    def delete_user(self, user_id):
        """ Удаление по telegram_id """
        self.cursor.execute(f"DELETE FROM user WHERE telegram_id = {user_id}")
        return self.conn.commit()

    def close(self):
        """ Закрываем соединение с БД """
        self.conn.close()

    def connect(self):
        """ Подключаемся к БД """
        self.conn = sqlite3.connect(self.name_db)
        self.cursor = self.conn.cursor()

    def make_xlsx(self):
        workbook = Workbook('KIFY_bot.xlsx')
        worksheet = workbook.add_worksheet()
        # Pass in the database path, db.s3db or test.sqlite
        mysel = self.cursor.execute("SELECT * FROM user")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        workbook.close()





