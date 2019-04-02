from flask import Flask
import json
import MySQLdb

app = Flask(__name__)

@app.route('/anomaly', methods = ['GET','POST'])
def hello_world():
    # data = json.loads(request.data)
    data = {}
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="student") 
    cur = db.cursor()
    # cur.execute("SELECT * FROM pacients")
    # print all the first cell of all the rows
    # a = list()
    # for i in cur.fetchall():
    #     a.append(i)
    data['weight'] = 122
    data['water'] = 10
    data['pulse'] = 90
    data['temperature'] = 30
    # insert into database
    command = "insert into pacients (weight, water, pulse, temperature) \
                 values(%s, %s, %s, %s)"
    arguments = (data['weight'], data['water'], data['pulse'], data['temperature'])

    cur.execute(command, arguments)

    return json.dumps(data)


if __name__=="__main__":
    app.run(debug=True)