#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import json

file = '/Users/anushka/Desktop/Colombia_input.json'

connection = mysql.connector.connect(host='localhost',
                             database='myflaskapp',
                             user='root',
                             password='rootroot')

with open(file) as data_file:
    data = json.load(data_file)

answers = data['answers']
variables = data['variables']
cursor = connection.cursor()

for key, value in answers.items():
    times = int(key) + 1

for i in range(0, times):
    ifpid = int(data["ifp_id"])
    format = str(variables['presidential_prime_ministerial'])
    country = str(variables['country'])
    date = str(variables['date_0'])
for key, value in answers.items():
    # store the list of matches played on this matchday
    candidateid = int(value['id'])
    candidatename = str(value['value'])
    candidatenumber = int(key) + 1
    print(candidatenumber,ifpid,country,format,date,candidateid,candidatename)
    # entry_exists = cursor.execute("SELECT ifpid,candidatename FROM candidates WHERE ifpid = %s AND candidatename = %s;",(ifpid,candidatename))
    # if entry_exists == 0:
    cursor.execute("INSERT INTO candidates(ifpid,country,format,date,candidatenumber,candidateid,candidatename) VALUES(%s, %s, %s,%s,%s,%s,%s)",(ifpid, country, format, date, candidatenumber, candidateid, candidatename))
    connection.commit()
    print ("Record inserted")

cursor.close()
connection.close()

