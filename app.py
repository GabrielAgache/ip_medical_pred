from flask import Flask, request
import json
import mysql.connector
import predict
from datetime import date
from flask_cors import CORS
import numpy as np


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello from flask'


def detect_outlier1(data_1):
    outliers = []
    threshold = 2
    mean_1 = np.mean(data_1)
    std_1 = np.std(data_1)

    for y in data_1:
        z_score = (y - mean_1) / std_1
        if np.abs(z_score) > threshold:
            outliers.append(y)
    return outliers


def detect_outlier2(data_1):
    outliers = []
    q1, q3 = np.percentile(data_1, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    for y in data_1:
        if y < lower_bound or y > upper_bound:
            outliers.append(y)

    return outliers


@app.route('/verify_anomaly', methods=['POST'])
def verify_anomaly():
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')

    cursor = cnx.cursor()

    data_dic = json.loads(request.data, encoding='UTF-8')
    response = {}
    if 'patient_id' not in data_dic:
        return json.dumps(data_dic)

    patient_id = data_dic['patient_id']

    for key in data_dic:
        if key == 'patient_id' or key == 'today':
            continue

        sql = ('select ' + key + ' from daily_data where patient_id = ' +
               str(patient_id) + ' order by day desc limit 10')

        cursor.execute(sql)
        result = cursor.fetchall()
        result = [line[0] for line in result]

        result.append(data_dic[key])

        outliers = detect_outlier1(result)

        if len(result) < 10 or data_dic[key] is None:
            response[key] = 'no data'
            continue

        if data_dic[key] in outliers:
            response[key] = 'anomaly'
        else:
            response[key] = 'ok'

    return json.dumps(response)


def to_mysql_date(today):
    day, month, year = today.split('-')
    day, month, year = int(day), int(month), int(year)
    return date(year, month, day)


@app.route('/send_data', methods=['POST'])
def send_data():
    data_dic = json.loads(request.data, encoding='UTF-8')
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor()

    patient_id = data_dic.get('patient_id')
    today = data_dic.get('today')

    today = to_mysql_date(today)

    if patient_id is None or today is None:
        return json.dumps({'message': 'Error! patient_id and \
                            today must be specified'})
    else:
        cursor.execute(
            'select * from daily_data where patient_id=%s \
             and day=%s', (patient_id, today))
        dup = cursor.fetchone()
        print(dup)
        if dup is not None:
            return json.dumps({'message': 'Error! patient already \
                                sent the data for today'})

    # daca nu gaseste cheia in dictionar initializeaza cu None by default
    pulse = data_dic.get('pulse', None)
    temperature = data_dic.get('temperature', None)
    water = data_dic.get('water', None)
    weight = data_dic.get('weight', None)
    calories = data_dic.get('calories', None)

    sql = ("INSERT INTO daily_data \
            (patient_id, water, weight, pulse, temperature, calories, day)\
            values (%s, %s, %s, %s, %s, %s, %s)")

    daily_data = (patient_id, water, weight, pulse,
                  temperature, calories, today)
    cursor.execute(sql, daily_data)
    cnx.commit()

    return json.dumps(data_dic)


@app.route('/predict_hd', methods=['POST'])
def get_result():
    data = json.loads(request.data)
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
        down = request.args.get('down', default=0, type=int)
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
        return json.dumps(get_pulse(min_pulse, max_pulse))
    if info == 'all':
        patient_id = request.args.get('id')
        today = request.args.get('day', default=None)
        if today is not None:
            day, month, year = today.split('-')
            day, month, year = int(day), int(month), int(year)
            today = date(year, month, day)
        return json.dumps(getPatientInfo(patient_id, today))


if __name__ == '__main__':
    app.run(debug=True)


def create_app(test_config=None):
    return app
