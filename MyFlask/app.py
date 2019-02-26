from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]
    return d


connect = sqlite3.connect('mySqlite.db')
# 指定工厂方法
connect.row_factory = dict_factory
cur = connect.cursor()
cur.execute("""SELECT * FROM MySqlite;""")
data = cur.fetchall()
print(len(data))
data1 = data[0:73]
data2 = data[73:141]
data3 = data[141:213]
data4 = data[213:307]



@app.route('/dream')
def dream():
    #   global data
    return render_template('index.html', data1=data1, data2=data2, data3=data3, data4=data4)


if __name__ == '__main__':
    app.run()
