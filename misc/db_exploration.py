"""
File for making sense of a database via python only
"""

import pandas as pd
import psycopg2

# Use `hidden.py` for credentials (but we could do other ways)
import hidden

# create db connection URI
db_connection_uri = hidden.psycopg2(hidden.secrets())

# create connection for "raw" SQL queries and cursor
conn = psycopg2.connect(db_connection_uri)
cur = conn.cursor()

# create another connection just for pandas work
pd_conn = psycopg2.connect(db_connection_uri)

# with "raw" SQL query, get table names
cur.execute("""SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';""")
table_names = [str(table).strip('(,)').strip("''") for table in cur.fetchall()]

def table_describe(table_name):
    query = f"""
    SELECT 
       table_name, 
       column_name, 
       data_type 
    FROM 
       information_schema.columns
    WHERE 
       table_name = '{table_name}';
    """
    table_describe_df = pd.read_sql(query, con=pd_conn)
    return table_describe_df

print(table_describe(table_name=table_names[0]))
#print(table_names[0])