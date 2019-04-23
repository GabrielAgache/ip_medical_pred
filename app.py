from flask import Flask, request
import json
import mysql.connector
import predict
from datetime import date
import predict


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello from flask'


id = 2


@app.route('/index', methods=['GET', 'POST'])
def index():
    data_dic = json.loads(request.data, encoding='UTF-8')
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    global id
    id += 1
    patient_id = 1
    cursor = cnx.cursor()
    calories = 1000
    pulse = data_dic['pulse']
    # steps = data_dic['steps']
    temperature = data_dic['temperature']
    today = data_dic['today']
    water = data_dic['water']
    weight = data_dic['weight']
    sql = ("INSERT INTO daily_data \
            (id, patient_id, water, weight, pulse, temperature, calories, day)\
            values (%s, %s, %s, %s, %s, %s, %s, %s)")
    day, month, year = today.split('-')
    day, month, year = int(day), int(month), int(year)
    today = date(year, month, day)

    daily_data = (id, patient_id, water, weight, pulse,
                  temperature, calories, today)
    cursor.execute(sql, daily_data)
    cnx.commit()

    print(data_dic)
    return json.dumps(data_dic)


@app.route('/predict_hd', methods=['POST'])
def get_result():
    data = request.get_json()
    return predict.classify(data, k=30)


@app.route('/get_pulse', methods=['GET'])
def get_pac_by_age():
    max_pulse = request.args.get('max_pulse')
    min_pulse = request.args.get('min_pulse')
    if min_pulse is None:
        min_pulse = 0
    if max_pulse is None:
        max_pulse = 200
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')

    cursor = cnx.cursor()

    sql = "SELECT patient_id from daily_data where pulse > %s and pulse < %s"
    cursor.execute(sql, (min_pulse, max_pulse))

    result = cursor.fetchall()
    res = [line[0] for line in result]
    res = list(set(res))

    return json.dumps(res)


@app.route('/get_day', methods=['GET'])
def get_day():
    today = request.args.get('day')
    day, month, year = today.split('-')
    day, month, year = int(day), int(month), int(year)
    today = date(year, month, day)
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT * from daily_data where day = %s"
    query_day = (today, )
    cursor.execute(sql, query_day)
    res = cursor.fetchall()
    for element in res:
        element['day'] = element['day'].strftime("%d-%m-%Y")
    return json.dumps(res)


@app.route('/get_calories', methods=['GET'])
def calories():
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor(dictionary=True)
    up = request.args.get('up', default=3000, type=int)
    down = request.args.get('down', default=1000, type=int)
    sql = ("SELECT patient_id from daily_data where calories < %s \
            and calories > %s")
    data = (up, down,)

    cursor.execute(sql, data)

    data_dic = cursor.fetchall()

    res = [line[0] for line in data_dic]
    res = list(set(res))

    return json.dumps(res)


@app.route('/get_water', methods=['GET'])
def water():
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor(dictionary=True)
    up = request.args.get('up', default=10, type=int)
    down = request.args.get('down', default=1, type=int)
    sql = ("SELECT patient_id from daily_data where water < %s \
            and water > %s")
    data = (up, down,)

    cursor.execute(sql, data)

    data_dic = cursor.fetchall()

    res = [line[0] for line in data_dic]
    res = list(set(res))

    return json.dumps(res)


@app.route('/get_weight', methods=['GET'])
def weight():
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor(dictionary=True)
    up = request.args.get('up', default=200, type=int)
    down = request.args.get('down', default=1, type=int)
    sql = ("SELECT patient_id from daily_data where weight < %s \
            and weight > %s")
    data = (up, down,)

    cursor.execute(sql, data)

    data_dic = cursor.fetchall()

    res = [line[0] for line in data_dic]
    res = list(set(res))

    return json.dumps(res)


@app.route('/get_info', methods=['GET'])
def getPatientInfo():
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor(dictionary=True)
    id = request.args.get('id')
    data = request.args.get('data', default=None)
    if data is None:
        sql = ("select * from daily_data where patient_id = %s ")
        daily_data = (id,)
        cursor.execute(sql, daily_data)
        records = cursor.fetchall()
    else:
        sql = ("select * from daily_data where patient_id = %s and day = %s")
        daily_data = (id, data)
        cursor.execute(sql, daily_data)
        records = cursor.fetchall()
    for element in records:
        element['day'] = element['day'].strftime("%d-%m-%Y")
    cnx.close()
    return json.dumps(records)


if __name__ == '__main__':
    app.run(debug=True)
