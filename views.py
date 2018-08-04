import sqlite3
import re
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

sqlite_path = 'db/todo.db'

date = '^\d{4}-\d{1,2}-\d{1,2}$';

def get_db_connection():
    connection = sqlite3.connect(sqlite_path)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    res = cursor.execute('SELECT * FROM todo')
    return render_template('index.html', todo_list=res.fetchall())

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == 'GET':
        todo = {}
        return render_template('edit.html', type='add', todo=todo)

    else:
        connection = get_db_connection()
        cursor = connection.cursor()
        error = []

        if not request.form['name']:
            error.append('タスク名を入力して下さい')
        if not re.match(date,request.form['duedate']):
            error.append('期日は『YYYY-M-D』で入力して下さい')

        if error:
            todo = request.form.to_dict()

            return render_template('edit.html', type='add', todo=todo, error_list=error)

        cursor.execute('INSERT INTO todo(name, duedate, memo) VALUES(?,?,?)',
                      (request.form['name'],
                      request.form['duedate'],
                      request.form['memo']))
        connection.commit()
        return redirect(url_for('index'))

@app.route("/delete/<int:id>")
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM todo WHERE id =?',(id,))
    connection.commit()
    return redirect(url_for('index'))


@app.route("/edit/<int:id>")
def edit(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    res = cursor.execute('SELECT * FROM todo WHERE id = ?', (id,))

    return render_template('edit.html', type='edit', todo=res.fetchone())



@app.route("/update/<int:id>", methods=['POST'])
def update_task(id):
    #空のerrorリストを作成→

    error = []
    # 入力項目が空欄（不備）があればerrorリストにコメントを格納
    if not request.form['name']:

        error.append('タスク名を入力して下さい')
    #if not request.form['duedate']:
        #error.append('期日を入力して下さい')
    if not re.match(date,request.form['duedate']):
            error.append('期日は『YYYY-M-D』で入力して下さい')
    # →errorリストにコメントが有るか確認。→あれば変数としてテンプレート(edit.html)のerror_listにわたす
    if error:
        todo = request.form.to_dict()

        todo['id'] = id
        return render_template('edit.html', type='edit', todo=todo, error_list=error)

    # →なければデータベースに接続し情報を更新
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('UPDATE todo set name = ? , duedate = ? , memo = ?, status = ? where id = ?',
                    (request.form['name'],
                    request.form['duedate'],
                    request.form['memo'],
                    request.form['status'],
                    id))
    connection.commit()
    return redirect(url_for('index'))
