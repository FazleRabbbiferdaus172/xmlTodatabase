import mysql.connector
import xml.etree.ElementTree as ET
from mysql.connector import errorcode
from configcon import conn
# ***************loading Xml file*****************
tree = ET.parse('new-books.xml')
root = tree.getroot()

# ***************table name*****************
table_name = root[0].tag


# **************attribute from XML
art_list = list(root[0].attrib.keys())

# **********************list of table name followed by coloumn name from Xml
col = [table_name]
for i in art_list:
    col.append(i)
for elem in root[0]:
    col.append(elem.tag)


# ******************making create table query
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

# *************************Getting Connection files****************


# *********************connecting database************************
db = conn()
print(db)
my_cursor = db.cursor()

# ********************creating table********************************
try:
    my_cursor.execute(new_query)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("already exists")
    else:
        print("err.msg")
else:
    print("ok")


# ******************geting the row values from xml*****************

# ****************improvement*****************
tree = ET.parse('new-books.xml')
new_root = tree.getroot()
list_of_value = []
value_tuple = []
col_new = col[1:]
subelem_tag_index = []
j = 0
for elem in root:
    value_tuple = ["Null"]*len(col_new)
    for i, a in enumerate(art_list):
        value_tuple[i] = str(elem.attrib[a])
    for subelem in elem:
        ind = col_new.index(subelem.tag)
        value_tuple[ind] = str(subelem.text)

    list_of_value.append(tuple(value_tuple))

# *******************Making insert query*******************
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

# ***********************inserting the rows********************
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
