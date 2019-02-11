import sys, mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import json


# def PrintFields(database, table):
""" Connects to the table specified by the user and prints out its fields in HTML format used by Ben's wiki. """

connection = mysql.connector.connect(host='localhost', database='myflaskapp', user='root', password='rootroot')
cursor = connection.cursor()
table = 'articleset'

sql = """ SHOW COLUMNS FROM %s """ % table
cursor.execute(sql)
fields=cursor.fetchall()
# print ('<table border="0"><tr><th>order</th><th>name</th><th>type</th><th>description</th></tr>')
# print ('<tbody>')
counter = 0
for field in fields:
    counter = counter + 1
    name = field[0]
    type = field[1]
    # print ('<tr><td>' + str(counter) + '</td><td>' + str(name) + '</td><td>' + str(type) + '</td><td></td></tr>')
# print ('</tbody>')
# print ('</table>')
cursor.close()
connection.close()

# users_database = sys.argv[1]
# users_table = sys.argv[2]
# print ("Wikified HTML for " + users_database + "." + users_table)
# print ("========================")
