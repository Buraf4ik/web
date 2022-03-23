from flask import Flask, render_template, url_for, request, escape, redirect
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


def recording_in_db(first_name, last_name, phone_number):
    connection = create_connection()
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
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dictionary")
    result = cursor.fetchall()
    user_list = []
    for val in result:
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


@app.route('/dictionary')
def dictionary():
    user_list = list_of_users()
    return render_template("database.html", user_list=user_list)


@app.route('/dictionary', methods=['POST'])
def add_request():
    first_name = request.form['first name']
    last_name = request.form['last name']
    number = request.form['number']
    if len(first_name) > 1 and len(last_name) > 1 and len(number) > 1:
        recording_in_db(first_name, last_name, number)
    else:
        print("введен пустой пользовтель")
    return render_template("database.html", user_list=list_of_users())


@app.route('/user')
@app.route('/user/<user_name>/<user_id>')
def user_redirect(user_name=None, user_id=None):
    print(user_name, user_id)
    connection = create_connection()
    insert_query = (
        f"SELECT COUNT(*) FROM dictionary WHERE (first_name = '{user_name}' and id = '{user_id}')")
    try:
        cursor = connection.cursor()
        cursor.execute(insert_query)
        connection.commit()
    except OperationalError:
        print('something went wrong')
    result = cursor.fetchone()[0]
    print(result)
    if result == 1:
        return render_template("user.html", username=user_name, id=user_id)
    else:
        return render_template("user.html", username=None, id=None)


@app.route('/user/<user_id>/delete')
def deletion(user_id=None):
    print(user_id)
    user_id = int(user_id)
    connection = create_connection()
    if connection is None:
        return False
    insert_query = (
        f"DELETE FROM dictionary WHERE (id = {user_id})")
    try:
        cursor = connection.cursor()
        cursor.execute(insert_query)
        connection.commit()
    except OperationalError:
        print('something went wrong')
    return redirect('/dictionary')


@app.route('/isak')
def isak():
    return render_template("isak.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
