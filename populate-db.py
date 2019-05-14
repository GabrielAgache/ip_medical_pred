import random
from datetime import date
import mysql.connector


def main():
    cnx = mysql.connector.connect(
        user='b380f338c76a8d', password='8768bb5c',
        host='eu-cdbr-west-02.cleardb.net', database='heroku_c4a6a99da4e3951')
    cursor = cnx.cursor()
    sql = ("INSERT INTO daily_data"
           " (patient_id, water, weight, pulse, temperature, calories, day)"
           " values (%s, %s, %s, %s, %s, %s, %s)")

    first_id = random.randint(10000, 80000)
    for i in range(1, 1000):
        patient_id = first_id + i
        weight = random.randint(1, 200)
        pulse = random.randint(60, 100)
        temperature = random.randint(35, 40)
        calories = random.randint(1000, 3000)
        year = random.randint(2015, 2018)
        month = random.randint(1, 12)
        day = random.randint(1, 22)
        for j in range(1, random.randint(1, 5)):
            water = random.randint(1, 10)
            weight = weight + random.random()
            pulse = pulse + random.random()
            calories = calories + random.randint(1, 500)
            temperature = temperature + random.random()
            insert_date = date(year, month, day + j)
            daily_data = (patient_id, water, weight, pulse,
                          temperature, calories, insert_date)
            cursor.execute(sql, daily_data)
            cnx.commit()
            print(daily_data)


if __name__ == '__main__':
    main()
