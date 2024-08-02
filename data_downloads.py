import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def download_csvs(detector_name, button_name):

    download_types = {
        'btn-download-24':'data_24h.csv',
        'btn-download-mov':'data_ma.csv',
        'btn-download-all':'data_all.csv',
    }
    # If button category available
    if button_name in download_types:

        # Create file name
        filename = f'{detector_name}_{download_types[button_name]}'

        # Calculate last 24 hours if requested

        # Read the CSV file into a pandas DataFrame from Database


        # *********** MUST BE EDITED/FIXED FOR DB ****************


        df = pd.read_csv(f"detector_data_test/{detector_name}-2022-05-15-to-2022-08-26.csv")

        # Convert the date column to datetime format
        df['date'] = pd.to_datetime(df['date'])


        # *********** MUST BE EDITED/FIXED FOR DB ****************



        # Slice the DataFrame to include only the last day of data
        df_last_day = df[-1440:]

        return df_last_day, filename
    
    else:

        return None
