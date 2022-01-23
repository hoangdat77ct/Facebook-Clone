import pymysql
import logging
logging.basicConfig(filename='../debug_log.log',level=logging.DEBUG)

def connect():
    db = None
    try:
        db = pymysql.connect(host="localhost",user="root",password="Hoangdat77ct",db="facebook_clone")
    except pymysql.connect.Error as e:
        logging.error(e)
    return db


def query_select(sql,values=None):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        res = cursor.fetchall()
        return res
    except pymysql.connect.Error as e:
        logging.error(e)
    finally:
        cursor.close()
        conn.close()


def query_CUD(sql, values=None):
    try:
        conn = connect()
        cursor = conn.cursor()
        res = cursor.execute(sql, values)
        conn.commit()
        return res
    except pymysql.connect.Error as e:
        logging.error(e)
    finally:
        cursor.close()
        conn.close()