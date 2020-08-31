import mysql.connector


def conn(h="localhost", u="root", p="1234", d="catalog"):
    db = mysql.connector.connect(
        host=h, user=u, password=p, database=d)

    return db
    #my_cursor = db.cursor()
