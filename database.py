''' 

File with all necessary functions for data download from server

'''
import pandas as pd
from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
import psycopg2


def format_sql(sql_data):
    ''' 
    Formats sql data fetched from table into datetime index and numeric column
    Args:       sql_data -> sqlalchemy row.Row object
    Returns:    pandas df

    '''
    # CSV file into a dataframe
    df = pd.DataFrame(sql_data)
    df = df.set_index('date')
    
    columns_types = df.dtypes.to_list()
    if len(set(columns_types)) > 1:
        for col in df.columns.to_list():
            df[col] = pd.to_numeric(df[col])
            
    return df

def connect_to_db():
    ''' 
    Creates an engine object based on sqlalchemy and psycopg2
    Args:       None
    Returns:    sqlalchemy engine

    '''
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

def connect_to_db_upload():
    ''' 
    Creates an engine object based on sqlalchemy and psycopg2
    Args:       None
    Returns:    sqlalchemy engine

    '''
    load_dotenv()
    DBNAME=getenv('DBNAME')
    DBUSER=getenv('DBUSER')
    DBHOST=getenv('DBHOST')
    DBPORT=getenv('DBPORT')
    DBPWRD=getenv('DBPWRD')

    try:
        connection_string = f'postgresql://{DBUSER}:{DBPWRD}@{DBHOST}:{DBPORT}/{DBNAME}'
        engine = create_engine(connection_string)

        print('Connected to muon database successfully')

    except:
        print('Unable to connect to muon database via sqlalchemy')
        engine = None
    
    try:
        conn = psycopg2.connect(f"dbname={DBNAME} user={DBUSER} host={DBHOST} port={DBPORT} password={DBPWRD}")
        print('Connected to muon database successfully')
    except:
        print('Unable to connect to muon database via psycopg2')
        conn = None

    return engine, conn