''' 

File with all necessary functions for data download from server

'''
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from os import getenv
from detector_info_settings.detector_format_settings import detector_settings
from datetime import date, timedelta
from sqlalchemy import create_engine
import psycopg2


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
