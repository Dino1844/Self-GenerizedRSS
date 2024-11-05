# db.py
import os
import sqlite3 as sql

pwd = os.path.dirname(os.path.abspath(__file__))+"\\"

def connect(db_name):
    path = pwd+ db_name 
    return sql.connect(path)
def new_cursor(conn):
    return conn.cursor()
def new_table_website(cursor,web_table_name,url_name="URL",web_name="WEB_NAME"):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS {}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {} TEXT UNIQUE,
            {} TEXT
        )
    """.format(web_table_name,url_name,web_name)
        
    )
def new_table_article(cursor, name, column1, column2, column3):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {} TEXT,
            {} TEXT UNIQUE,
            {} TEXT
        )
    """.format(name, column1, column2, column3)
    )
def get_index(cursor,website_name,table_name = "rss_feeds"):
    cursor.execute("""
            SELECT id 
            FROM {}
            WHERE URL = '{}'                      
     """.format(table_name,website_name)
        
    )
    return cursor.fetchone()[0]
def get_url(cursor,num,title):
    cursor.execute("""
        SELECT link FROM {} WHERE title = {}
    """.format(f"web{num}",f"{title}"))
    
    return cursor.fetchone()
def get_title_fromall(cursor):
    titles = []
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE '%web%'
    """)
    tables = cursor.fetchall()
    i = 1
    for table in tables:
        cursor.execute("""
            SELECT title 
            FROM {}
        """.format(table[0])
       )
        titles = cursor.fetchall()
        titles.insert(0,table)
        i+=1
    titles.append((f"web{i}",))

    return titles


#测试代码
#conn = connect("rss.db")
#cursor = new_cursor(conn)



