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

@app.route('/index', methods=['GET', 'POST'])
def index():
    data_dic = json.loads(request.data, encoding='UTF-8')
    cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='medicad')
    patient_id = 1
    cursor = cnx.cursor()
    calories = 1000
    pulse = data_dic['pulse']
    steps = data_dic['steps']
    temperature = data_dic['temperature']
    today = data_dic['today']
    water = data_dic['water']
    weight = data_dic['weight']
    sql = ("INSERT INTO daily_data"
        " (patient_id, water, weight, pulse, temperature, calories, day)" 
        " values (%s, %s, %s, %s, %s, %s, %s)")
    day, month, year = today.split('-')
    day, month, year = int(day), int(month), int(year)
    today = date(year, month, day)

    daily_data = (patient_id, water, weight, pulse, temperature, calories, today)
    cursor.execute(sql, daily_data)
    cnx.commit()

    print(data_dic)
    return json.dumps(data_dic)
    

@app.route('/predict_hd', methods=['POST'])
def get_result():
    data = request.get_json()
    return predict.classify(data, k=30)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)