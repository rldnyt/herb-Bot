import sqlite3
import smtplib
from email.mime.text import MIMEText
import asyncio

class botsetup:
    version = "3.1.0 - 2020 12 08 release"

class Color:
    red = 0xff1812
    orange = 0xfa972e
    yellow = 0xFED000
    green = 0x9cfa47
    blue = 0x80f8fa
    dark_blue = 0x2674fa
    purple = 0xc2abf7
    pink = 0xf7abc7
    white = 0xFFFFFF
    dark_embed = 0x2f3136
    white_embed = 0xF2F3F5

class database:
    class add:
        def table(self, dbfile, tablename, tabledata):
            conn = sqlite3.connect(f"{dbfile}.db")
            cur = conn.cursor()
            cur.execute(f'''CREATE TABLE IF NOT EXISTS {tablename}({tabledata})''')
            conn.commit()
            cur.close()
            conn.close()
        def data(self, dbfile, tablename, tabledata_the_number ,data):
            conn = sqlite3.connect(f"{dbfile}.db")
            cur = conn.cursor()
            cur.execute(f'''INSERT INTO {tablename} VALUES({tabledata_the_number})''', (data))
            conn.commit()
            cur.close()
            conn.close()
    class removal:
        def table(self, dbfile, tablename):
            conn = sqlite3.connect(f"{dbfile}.db")
            cur = conn.cursor()
            cur.execute(f'Drop Table If Exists {tablename}')
            conn.commit()
            cur.close()
            conn.close()
        def data(self, dbfile, tablename, dataname, data):
            conn = sqlite3.connect(f"{dbfile}.db")
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {tablename} WHERE {dataname}", (data,))
            conn.commit()
            cur.close()
            conn.close()
        def table_data_all(self, dbfile, tablename):
            conn = sqlite3.connect(f"{dbfile}.db")
            cur = conn.cursor()
            conn.execute(f"delete from {tablename}")
            conn.commit()
            cur.close()
            conn.close()
        def table_data_all_print(self, dbfile, tablename):
            conn = sqlite3.connect(f"{dbfile}.db")
            cur = conn.cursor()
            print(f"{tablename} DB 데이터 모든데이터 제거 : ", conn.execute(f"delete from {tablename}").rowcount, "개")
            conn.commit()
            cur.close()
            conn.close()
    class update:
        def data(self, dbfile, tablename, dataname, data, tabledata_the_number, tabledata): # tabledata_the_number = ?,?,? <- 이거
            conn = sqlite3.connect(f"{dbfile}.db")
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {tablename} WHERE {dataname}", (data,))
            cur.execute(f'''INSERT INTO {tablename} VALUES({tabledata_the_number})''', (tabledata))
            conn.commit()
            cur.close()
            conn.close()

class email:

    def __init__(self, email:str, password:str, subject:str, to:str, From:str, content:str, Fromname=None, mode=None):
        """
        ---mode----
        없을경우 : TEXT
        HTML : HTML으로 보내짐니다.
        """
        self.email = email
        self.password = password
        self.subject = subject
        self.to = to
        self.From = From
        self.content = content
        self.Fromname = Fromname
        self.mode = mode

    def google(self):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.email, self.password)
        if self.mode == "HTML" or self.mode == "html": msg = MIMEText(self.content, _subtype = 'html', _charset = 'utf-8')
        else: msg = MIMEText(self.content)
        msg['Subject'] = self.subject
        msg['To'] = self.to
        if not self.Fromname is None: msg['From'] = self.Fromname
        s.sendmail(self.From, self.to, msg.as_string())
        s.quit()
    def naver(self):
        s = smtplib.SMTP('smtp.naver.com', 465)
        s.starttls()
        s.login(self.email, self.password)
        msg = MIMEText(self.content)
        msg['Subject'] = self.subject
        msg['To'] = self.to
        if not self.Fromname is None: msg['From'] = self.Fromname
        s.sendmail(self.From, self.to, msg.as_string())
        s.quit()


