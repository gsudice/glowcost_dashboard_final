''' 

File with all necessary functions for data download from server

'''
import pandas as pd
from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine


def format_sql(sql_data):
    ''' 
    Formats sql data fetched from table into datetime index and numeric column
    Args:       sql_data -> sqlalchemy row.Row object
    Returns:    pandas df

    '''
    # CSV file into a dataframe
    df = pd.DataFrame(sql_data)
    df = df.set_index('date')
    return df

def connect_to_db():
    # Extract environment variables
    load_dotenv()
    DBNAME=getenv('DBNAME')
    DBUSER=getenv('DBUSER')
    DBHOST=getenv('DBHOST')
    DBPORT=getenv('DBPORT')
    DBPWRD=getenv('DBPWRD')

    try:
        connection_string = f'postgresql+psycopg2://{DBUSER}:{DBPWRD}@{DBHOST}:{DBPORT}/{DBNAME}'
        conn = create_engine(connection_string)

        print('Connected to muon database successfully')
        return conn

    except:
        print('Unable to connect to muon database')
        return None
