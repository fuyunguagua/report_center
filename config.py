import MySQLdb

class Constant:

    #database
    HOST = 'localhost'
    USER = 'toor'
    PASS = '12345678'

    PIROR_WATERMARK = 0

db = MySQLdb.connect(Constant.HOST, Constant.USER, Constant.PASS)

def newDB():
    return MySQLdb.connect(Constant.HOST, Constant.USER, Constant.PASS)

def init_database():
    cursor = db.cursor()
    try:
        cursor.execute("create database if "
                       "not exists track_report;")
    except Exception as e:
        pass

    db.select_db("track_report")
    sql = """CREATE TABLE RECORD(
             ID INT NOT NULL AUTO_INCREMENT,
             TIMESTAMP VARCHAR(20),
             WATERMARK VARCHAR(10),
             SRC_IP VARCHAR(20),
             DST_IP VARCHAR(20),
             CUR_IP VARCHAR(20),
             PRIMARY KEY (ID))
             """
    try:
        cursor.execute(sql)
    except Exception as e:
        pass

    sql = """CREATE TABLE ipInfo(
             ID INT NOT NULL AUTO_INCREMENT,
             IP VARCHAR(20),
             LOCATION VARCHAR(20),
             LON VARCHAR(20),
             LAT VARCHAR(20),
             PRIMARY KEY (ID))
             """

    try:
        cursor.execute(sql)
    except Exception as e:
        pass

init_database()