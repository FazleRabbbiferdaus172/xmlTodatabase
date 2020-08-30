import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector.errors import Error
from mysql.connector import errorcode
tree = ET.parse('books.xml')
root = tree.getroot()

table_name = root.tag  # table name
# print(len(root))
# print(root[0].tag)
a = str(list(root[0].attrib.keys())[0])  # first col : id
# print(a)  # key name = id  <- first col_name in table

col = [a]  # adding first coloumn name to a list

# ***printing the id values*****
#id_values = []
'''for elem in root:
     # print(elem.attrib[a])
    id_values.append(str(elem.attrib[a]))'''

# ****rest of the col_name**********
for elem in root[0]:
    col.append(elem.tag)
    # print(elem.tag)

# print(col)  # all coloumns from xml file for table


# ***********connecting database***********************
db = mysql.connector.connect(
    host="localhost", user="root", password="1234", database="catalog")

# print(db)  # if the connection is set up
mycursor = db.cursor()

# *****************Printing all database name***********************
#mycursor.execute("SHOW DATABASES")

#databases = mycursor.fetchall()
# print(databases)

# ***************************Creating the table********************************
# mycursor.execute(
#    "CREATE TABLE {} ({} VARCHAR(255)  PRIMARY KEY, {} VARCHAR(255), {} VARCHAR(255), {} VARCHAR(255),{} VARCHAR(255),{} VARCHAR(255),{} VARCHAR(255))".format(table_name, col[0], col[1], col[2], col[3], col[4], col[5], col[6],))


# ******************printinf all the table in database**********************************
#mycursor.execute("SHOW TABLES")

#tables = mycursor.fetchall()

'''for table in tables:
    # print(table)'''

# ************************printing all the coloumn in table************************************
#mycursor.execute("DESC {}".format(table_name))

#table_col = mycursor.fetchall()

# print(table_col)


# *******************************Inserting rows into the table**************
list_of_value = []
value_tuple = []
test = [("5", "a", "a", "a", "a", "a", "a"),
        ("6", "a", "a", "a", "a", "a", "a")]
for elem in root:
    value_tuple = []
    value_tuple.append(str(elem.attrib[a]))
    for subelem in elem:
        value_tuple.append(str(subelem.text))
    list_of_value.append(tuple(value_tuple))

# print(list_of_value)
# print(id_values)

query = "INSERT INTO {} ({}, {}, {}, {}, {}, {}, {} ) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(
    table_name, col[0], col[1], col[2], col[3], col[4], col[5], col[6])


# print(query)

mycursor.executemany(query, test)

db.commit()

print(mycursor.rowcount, "records inserted")
