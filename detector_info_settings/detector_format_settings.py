''' 
This file contains important settings for each monitor data including:
    - number of splits necessary to format string data within df's initial one column 'counts'
    - which of the three values produced by monitor will be considered the real 'counts'
    - what column number holds the real 'counts' value based on splits made within string
    - what column number holds 'date' data based on splits made within string
    - what 'timezone' is assigned to each monitor for localization before making into UTC
    - what frequency 'freq' does the data coming from the monitor have (usually every minute)
'''
detector_settings = {
        '2Paddle': {'splits':3, 'counts_val':1, 'counts_col':0, 'date_col':3, 'timezone':'America/New_York', 'freq':'1min'}, 
        '4Paddle': {'splits':3, 'counts_val':1, 'counts_col':0, 'date_col':3, 'timezone':'America/New_York', 'freq':'1min'},
        'MarkV': {'splits':3, 'counts_val':1, 'counts_col':0, 'date_col':3, 'timezone':'America/New_York', 'freq':'1min'},
        'Abuja': {'splits':3, 'counts_val':2, 'counts_col':1, 'date_col':3, 'timezone':'Africa/Lagos', 'freq':'1min'},
        'APO': {'splits':3, 'counts_val':2, 'counts_col':1, 'date_col':3, 'timezone':'US/Mountain', 'freq':'1min'},
        'Chara_Muon002': {'splits':11, 'counts_val':1, 'counts_col':4,  'date_col':0, 'timezone':'America/Los_Angeles', 'freq':'1min'},
        'ColomboV1': {'splits':11, 'counts_val':1, 'counts_col':4,  'date_col':0, 'timezone':'Asia/Colombo', 'freq':'1min'},
        'ColomboV2': {'splits':5, 'counts_val':1, 'counts_col':2,  'date_col':5, 'timezone':'Asia/Colombo', 'freq':'1min'},
        'OneParkPlace': {'splits':5, 'counts_val':1, 'counts_col':2, 'date_col':5, 'timezone':'America/New_York', 'freq':'1min'},
        'Rm415_Muon001': {'splits':3, 'counts_val':1, 'counts_col':0, 'date_col':3, 'timezone':'America/New_York', 'freq':'1min'},
        'SantaMarta': {'splits':3, 'counts_val':1, 'counts_col':0, 'date_col':3, 'timezone':'America/Bogota', 'freq':'1min'},
        'Serbia_BelgradeDet1':{'splits':4, 'counts_val':1, 'counts_col':1, 'date_col':4, 'timezone':'Europe/Belgrade', 'freq':'1min'},
        'Serbia_BelgradeDet2':{'splits':4, 'counts_val':1, 'counts_col':1, 'date_col':4, 'timezone':'Europe/Belgrade', 'freq':'1min'},
        'UvaWellassa_Muon001':{'splits':11, 'counts_val':1, 'counts_col':4, 'date_col':0, 'timezone':'Asia/Colombo', 'freq':'1min'},
    }