import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SQLiteDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.con.close()

    def query_db(self, query, one=False):
        result =  self.cur.execute(query).fetchall()
        return (result[0] if result else None) if one else result

    def insert_into_db(self, table_name, params):
        columns = ', '.join(params.keys())
        values = ', '.join([f'"{str(i)}"' for i in params.values()])
        self.cur.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")

    def select_from_db(self, table_name, columns:list, where=None, one=False):
        columns = ', '.join(columns)
        query = f"SELECT {columns} FROM {table_name}"
        if where:
            where = ', '.join([f"{key}='{value}'" for key, value in where.items()])
            query += f' WHERE {where}'
        return self.query_db(query, one)

