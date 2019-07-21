import sqlite3
import pandas as pd
import contextlib

class SQLiteDB(object):
    
    def __init__(self, db_path):
        
        self.conn = sqlite3.connect(db_path)
    
    @contextlib.contextmanager
    def cursor(self):
        
        cursor = self.conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
            self.conn.commit()
            
    def drop(self, table_name):
        
        sql = 'DROP TABLE {table_name}'.format(
            table_name=table_name)
        
        with self.cursor() as c:
            c.execute(sql)
    
    def create(self, table_name, columns, types):
        
        cols_types = ', '.join(
            [c + ' ' + d for c, d in zip(columns, types)])
        sql = 'CREATE TABLE {table_name} ({cols_dtypes})'.format(
            table_name=table_name, 
            cols_dtypes=cols_types)
        
        with self.cursor() as c:
            c.execute(sql)
    
    def insert(self, table_name, df):
        
        data = [tuple(row) for row in df.to_dict('split')['data']]
        holders = ', '.join(['?'] * len(df.columns))
        sql = 'INSERT INTO {table_name} VALUES ({holders})'.format(
            table_name=table_name, 
            holders=holders)
        
        with self.cursor() as c:
            c.executemany(sql, data)
        
    def update(self, table_name, columns, values, options=''):
        
        holders = ', '.join([c + ' = ?' for c in columns])
        sql = 'UPDATE {table_name} SET {holders} {options}'.format(
            table_name=table_name, 
            holders=holders, 
            options=options)
        
        with self.cursor() as c:
            c.execute(sql, tuple(values))
        
    def select(self, table_name, columns='*', options=''):
        
        sql = 'SELECT {columns} FROM {table_name} {options}'.format(
            columns=', '.join(columns),
            table_name=table_name,
            options=options)
        
        with self.cursor() as c:
            c.execute(sql)
            data = c.fetchall()
        
        if columns == '*':
            columns = self.columns(table_name)
            
        df = pd.DataFrame(data=data, columns=columns)
        
        return df
    
    
    def columns(self, table_name):
        
        sql = 'PRAGMA table_info({})'.format(table_name)
        with self.cursor() as c:
            c.execute(sql)
            col_infos = c.fetchall()
            
        columns = [i[1] for i in col_infos]
        return columns
             
    def close(self):
        
        self.conn.close()