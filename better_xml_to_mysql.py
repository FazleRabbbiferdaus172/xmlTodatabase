import mysql.connector
import xml.etree.ElementTree as ET
from mysql.connector import errorcode


tree = ET.parse('books.xml')
root = tree.getroot()

id_by = '<'+str(root[0].tag)+'>'
print(id_by)
table_name = root.tag

art_list = list(root[0].attrib.keys())
col = [table_name]
for i in art_list:
    col.append(i)
for elem in root[0]:
    col.append(elem.tag)

new_query = "CREATE TABLE {0} ("
add_query = "} VARCHAR(255) "
for i in range(1, len(col)):
    new_query += "{" + str(i) + add_query
    if i == 1:
        new_query += "PRIMARY KEY"
    if i != len(col) - 1:
        new_query += ","
new_query += ")"

new_query = new_query.format(*col)

db = mysql.connector.connect(
    host="localhost", user="root", password="1234", database="catalog")

my_cursor = db.cursor()

try:
    my_cursor.execute(new_query)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("already exists")
    else:
        print("err.msg")
else:
    print("ok")


"INSERT INTO {} ({}, {}, {}, {}, {}, {}, {} ) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(
    table_name, col[0], col[1], col[2], col[3], col[4], col[5], col[6])


list_of_value = []
value_tuple = []
a = str(list(root[0].attrib.keys())[0])
for elem in root:
    value_tuple = []
    value_tuple.append(str(elem.attrib[a]))
    for subelem in elem:
        value_tuple.append(str(subelem.text))
    list_of_value.append(tuple(value_tuple))

new_query = "INSERT INTO {0} ("
add_query = "}"
for i in range(1, len(col)):
    new_query += "{" + str(i) + add_query
    if i != len(col) - 1:
        new_query += ","
new_query += ")"
new_query += " VALUES ("

for i in range(1, len(col)):
    new_query += "%s"
    if i != len(col) - 1:
        new_query += ","
new_query += ")"
new_query = new_query.format(*col)

try:
    my_cursor.executemany(new_query, list_of_value)
    db.commit()
    print(my_cursor.rowcount, "records inserted")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("already exists")
    else:
        print(err.msg)
        print(err.errno)
else:
    print("ok")
