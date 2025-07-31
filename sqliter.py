import sqlite3
import config

class DBConnection(object):
    def __init__(self):
        self.conn = sqlite3.connect(f'{config.DIR}database.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.update_db()  # Добавляем вызов метода для обновления структуры таблицы
    
    def update_db(self):
        # Добавляем столбцы, если они еще не существуют
        try:
            self.c.execute('ALTER TABLE CHANNELS ADD COLUMN SPAM_ENABLED INTEGER DEFAULT 1')
        except sqlite3.OperationalError:
            pass  # Колонка уже существует

        try:
            self.c.execute('ALTER TABLE CHANNELS ADD COLUMN TIMEOUT INTEGER DEFAULT 5')
        except sqlite3.OperationalError:
            pass  # Колонка уже существует

        self.conn.commit()
    
    def add_additional_text(self, id , text):
        table = self.c.execute(f'SELECT ADDITIONAL FROM CHANNELS WHERE CHANNEL = "{id}"').fetchone()
        if table == None:
            self.c.execute(f'INSERT INTO CHANNELS(CHANNEL, ADDITIONAL) VALUES (?,?)', [str(id), str(text)])
        else:
            self.c.execute(f'UPDATE CHANNELS SET ADDITIONAL = (?) WHERE CHANNEL = (?)', [str(text),str(id)])
        self.conn.commit()
    
    def get_additional_text(self, id):
        table = self.c.execute(f'SELECT ADDITIONAL FROM CHANNELS WHERE CHANNEL = "{id}"').fetchone()
        return table
    
    def change_text(self, text):
        self.c.execute(f'UPDATE SETTINGS SET TEXT = (?) WHERE ID = (?)', [str(text), 1])
        self.conn.commit()
    
    def change_photo(self, name):
        self.c.execute(f'UPDATE SETTINGS SET PHOTO = (?) WHERE ID = (?)', [str(name), 1])
        self.conn.commit()
    
    def settings(self):
        table = self.c.execute(f'SELECT * FROM SETTINGS WHERE ID = (?)', [1]).fetchone()
        return table
    
    def setSpam(self, spam):
        self.c.execute(f'UPDATE SETTINGS SET SPAM = (?) WHERE ID = (?)', [spam, 1])
        self.conn.commit()
    
    def setTimeOut(self, time):
        self.c.execute(f'UPDATE SETTINGS SET TIMEOUT = (?) WHERE ID = (?)', [time, 1])
        self.conn.commit()
    
    # New methods
    def stop_spam_for_channel(self, channel_id):
        self.c.execute(f'UPDATE CHANNELS SET SPAM_ENABLED = 0 WHERE CHANNEL = (?)', [str(channel_id)])
        self.conn.commit()
    
    def set_channel_timeout(self, channel_id, timeout):
        self.c.execute(f'UPDATE CHANNELS SET TIMEOUT = (?) WHERE CHANNEL = (?)', [timeout, str(channel_id)])
        self.conn.commit()
    
    def __del__(self):
        self.c.close()
        self.conn.close()

# Пример использования:
db = DBConnection()
