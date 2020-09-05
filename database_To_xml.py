from lxml import etree
from lxml.builder import E as buildE
import mysql.connector
from configcon import conn

# ***************XMl builder***************


def E(tag, parent=None, attr=None, value=None, content=None):
    if attr is None:
        element = buildE(tag)
    else:
        element = buildE(tag, value)
    if content is not None:
        element.text = content
    if parent is not None:
        parent.append(element)
    return element


def fetchXML(db_name, tbl_name, fields, rows):
    #fields = [x[0] for x in cursor.description]
    doc = E(db_name)  # database name
    for record in rows:  # rows
        attr = str(fields[0])
        value = str(record[0])
        va = dict()
        va[attr] = value
        r = E(tbl_name, parent=doc, attr=attr, value=va)  # table name
        for (k, v) in zip(fields[1:], record[1:]):  # cols,row
            E(k, content=v, parent=r)
    return doc


# *********************connecting database************************
db = conn()
print(db)
database_name = 'catalog'
table_name = 'book'
my_cursor = db.cursor()
query1 = "SHOW COLUMNS FROM book"
query2 = "select * from book"
my_cursor.execute(query1)
dummy = my_cursor.fetchall()
cols = []
for i in dummy:
    cols.append(i[0])
my_cursor.execute(query2)
rows = my_cursor.fetchall()
# print(cols)
# print(rows)
doc = fetchXML(database_name, table_name, cols, rows)
result = str(etree.tostring(doc, pretty_print=True), 'utf-8')
print(result)
with open('new_book_xml.xml', 'w') as ouf:
    ouf.write('<?xml version="1.0"?>'+'\n')
    ouf.write(result)
