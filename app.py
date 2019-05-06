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



def get_pulse(min_pulse, max_pulse):
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')

    cursor = cnx.cursor()

    sql = "SELECT patient_id from daily_data where pulse >= %s and pulse <= %s"
    cursor.execute(sql, (min_pulse, max_pulse))

    result = cursor.fetchall()
    res = [line[0] for line in result]
    res = list(set(res))

    return res

def get_day(today):
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
    return res


def calories(up, down):
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor(dictionary=True)
    sql = ("SELECT patient_id from daily_data where calories <= %s \
            and calories > %s")
    data = (up, down,)

    cursor.execute(sql, data)

    data_dic = cursor.fetchall()

    res = [line['patient_id'] for line in data_dic]
    res = list(set(res))

    return res


def water(up, down):
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor(dictionary=True)
    sql = ("SELECT patient_id from daily_data where water <= %s \
            and water > %s")
    data = (up, down,)

    cursor.execute(sql, data)

    data_dic = cursor.fetchall()

    res = [line['patient_id'] for line in data_dic]
    res = list(set(res))

    return res


def weight(up, down):
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor(dictionary=True)
    sql = ("SELECT patient_id from daily_data where weight <= %s \
            and weight > %s")
    data = (up, down,)

    cursor.execute(sql, data)

    data_dic = cursor.fetchall()

    res = [line['patient_id'] for line in data_dic]
    res = list(set(res))

    return res

def getPatientInfo(id, data):
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor(dictionary=True)
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
    return records

@app.route('/get', methods=['GET'])
def get():
    info = request.args.get('info')
    if info == 'weight':
        up = request.args.get('up', default=200, type=int)
        down = request.args.get('down', default=1, type=int)
        return json.dumps(weight(up, down))
    if info == 'water':
        up = request.args.get('up', default=10, type=int)
        down = request.args.get('down', default=1, type=int)
        return json.dumps(water(up, down))
    if info == 'calories':
        up = request.args.get('up', default=3000, type=int)
        down = request.args.get('down', default=1000, type=int)
        return json.dumps(calories(up, down))
    if info == 'day':
        today = request.args.get('day')
        day, month, year = today.split('-')
        day, month, year = int(day), int(month), int(year)
        today = date(year, month, day)
        return json.dumps(get_day(today))
    if info == 'pulse':
        max_pulse = request.args.get('max', default=200, type=int)
        min_pulse = request.args.get('min', default=0, type=int)
        return json.dumps(get_pulse(min, max))
    if info == 'all':
        id = request.args.get('id')
        today = request.args.get('day', default=None)
        if today is not None:
            day, month, year = today.split('-')
            day, month, year = int(day), int(month), int(year)
            today = date(year, month, day)
        return json.dumps(getPatientInfo(id, today))



if __name__ == '__main__':
    app.run(debug=True)
