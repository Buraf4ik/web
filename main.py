from flask import Flask, render_template, url_for, request, escape
import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name='web2', db_user='postgres', db_password='ehjd2001',
                      db_host='127.0.0.1', db_port='5432'):
    # Функция, осуществляющая подключение к базе данных
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print('Connected to database')
    except OperationalError:
        print('an operating error has occurred')
    return connection


#
#
# create_connection('web2', 'postgres', 'ehjd2001', '127.0.0.1', '5432')


def being_in_db(stud):
    connection = create_connection('web2', 'postgres', 'ehjd2001', '127.0.0.1', '5432')
    if connection is None:
        return False
    cursor = connection.cursor()
    # cursor -объект делающий запросы в бд и получающий их результаты
    cursor.execute('SELECT * FROM dictionary')
    result = cursor.fetchall()
    # fetchall возвращает список кортежей.Последовательная строка где каждая строка представляет собой последовательность элементов в столбцах.
    if len(result) == 0:
        return False
    # если записи нет, то возвращает false
    summ = []
    for user in result:
        user = list(user)
        summ1 = []
        for val in user:
            summ1.append(val.strip())
        summ.append(summ1)
    for st in summ:
        if ' '.join(st) == stud:
            # пробел между каждой записью
            return True
    return False


def recording_in_db(first_name, last_name, phone_number):
    connection = create_connection('web2', 'postgres', 'ehjd2001', '127.0.0.1', '5432')
    if connection is None:
        return False
    insert_query = (
        f"INSERT INTO dictionary (first_name, last_name, phone_number) VALUES ('{first_name}', '{last_name}', '{phone_number}')")
    try:
        cursor = connection.cursor()
        cursor.execute(insert_query)
        connection.commit()
    except OperationalError:
        print("wrong input")


def list_of_users():
    connection = create_connection('web2', 'postgres', 'ehjd2001', '127.0.0.1', '5432')
    if connection is None:
        return False
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dictionary")
    result = cursor.fetchall()
    total = []
    for user in result:
        total.append(list(user))

    user_list = []
    for val in total:
        user_list.append({
            'user id': str(val[0]), 'first name': val[1],
            'last name': val[2], 'phone number': val[3]
        })
    return user_list


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/oop')
def oop():
    return render_template("oop.html")


@app.route('/dictionary')
def dictionary():
    user_list = list_of_users()
    return render_template("database.html", user_list=user_list)


@app.route('/dictionary', methods=['POST'])
def add_request():
    first_name = request.form['first name']
    last_name = request.form['last name']
    number = request.form['number']
    recording_in_db(first_name, last_name, number)
    user_list = list_of_users()
    return render_template("database.html", user_list=user_list)


@app.route('/user/')
@app.route('/user/<user_name>/<user_id>')
def user_redirect(user_name=None, user_id=None):
    if user_name == "":
        user_name = None
    return render_template("user.html", username=user_name, id=user_id)


@app.route('/dictionary')
def deletion(user_id, user_name):
    user_id = int(user_id)
    connection = create_connection()
    if connection is None:
        return False
    insert_query = (
        f"DELETE FROM dictionary WHERE ('first_name' = {user_name} , 'id' = {user_id})")

    try:
        cursor = connection.cursor()
        cursor.execute(insert_query)
        connection.commit()
    except OperationalError:
        print('something went wrong')
    dictionary()


@app.route('/isak')
def isak():
    return render_template("isak.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
