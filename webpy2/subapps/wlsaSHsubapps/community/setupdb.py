import sqlite3
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, parent_dir)
import config

def execute_sql_file(filename):
    conn = sqlite3.connect(config.DB_LOC)
    cursor = conn.cursor()
    
    with open(filename, 'r', encoding='utf-8') as f:
        sql_script = f.read()
        
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

# 执行 setup.sql 文件
execute_sql_file(config.CURRENT_DICTORY + r"\subapps\wlsaSHsubapps\community\schema.sql")
