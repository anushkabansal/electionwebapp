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


# cursor.execute("DROP TABLE if EXISTS articles;")
# connection.commit()
# cursor.execute("CREATE TABLE IF NOT EXISTS articles(id INT(11) AUTO_INCREMENT PRIMARY KEY,ifpid  INT(11),country  TEXT(20),format  TEXT(20),date  DATE,polldate DATE , fieldworkdate DATE , pollingfirm TEXT, samplesize INT(11),moe FLOAT (11));")
# connection.commit()

# query2 = "DROP TABLE `%s`"
# cursor.execute(query2,([country+'-'+date]))
# connection.commit()

# cursor.execute("DROP TABLE `{}`".format(country+'-'+date))
# connection.commit()

# cursor.execute("CREATE TABLE IF NOT EXISTS`{}` (id INT(11) AUTO_INCREMENT PRIMARY KEY,ifpid  INT(11),country  TEXT(20),format  TEXT(20),date  DATE,polldate DATE , fieldworkdate DATE , pollingfirm TEXT, samplesize INT(11),moe FLOAT (11))".format(country+'-'+date))
# # # cursor.execute(query1,[country+'-'+date])
# connection.commit()

for key, value in answers.items():
    # store the list of matches played on this matchday
    candidateid = int(value['id'])
    candidatename = str(value['value'])
    candidatenumber = int(key) + 1
    print(candidatenumber,ifpid,country,format,date,candidateid,candidatename)

    # query = "ALTER TABLE `%s` ADD COLUMN `%s` VARCHAR(20) NOT NULL"
    # cursor.execute("ALTER TABLE `{}` ADD COLUMN`{}` VARCHAR(20) NOT NULL".format(country+'-'+date,candidatename))
    # connection.commit()

    #to check table use query
    #DESCRIBE `colombia-2018-06-17`;

    # cursor.execute("ALTER TABLE articles ADD COLUMN `{}` VARCHAR(20) NULL".format(candidatename))
    # connection.commit()


    cursor.execute(
        "REPLACE INTO candidates (ifpid,country,format,date,candidatenumber,candidateid,candidatename) VALUES(%s, %s, %s,%s,%s,%s,%s)",
        (ifpid, country, format, date, candidatenumber, candidateid, candidatename))
    connection.commit()

    print ("Record inserted")

cursor.close()
connection.close()

