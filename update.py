import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by the db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
   except Error as e:
       print(e)

   return conn

def create_tables(conn):
    """ Create 'projects' and 'tasks' tables if they do not exist """
    try:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        start_date TEXT,
                        end_date TEXT
                    )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        project_id INTEGER,
                        name TEXT NOT NULL,
                        description TEXT,
                        status TEXT,
                        start_date TEXT,
                        end_date TEXT,
                        FOREIGN KEY (project_id) REFERENCES projects (id)
                    )''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def update(conn, table, id, **kwargs):
   """
   update status, begin_date, and end date of a task
   :param conn:
   :param table: table name
   :param id: row id
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

if __name__ == "__main__":
   conn = create_connection("database.db")
   update(conn, "tasks", 2, status="started")
   update(conn, "tasks", 2, stat="started")
   conn.close()
