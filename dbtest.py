import sqlite3
import re
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

sqlite_path = 'db/todo.db'


# duedateの入力形式を定める正規表現
date = '^\d{4}-\d{1,2}-\d{1,2}$';

connection = sqlite3.connect(sqlite_path)
c = connection.cursor()

c.execute('create table todo (id INTEGER PRIMARY KEY,name varchar(64), duedate varchar(64), memo varchar(64), status varchar(64))')
sql = "insert into todo values(1,'pythonやる','2018-8-4','毎日継続！','未完了')"
c.execute(sql)

connection.commit()
connection.close()
