import pandas as pd

def load_data():
    data_path = 'D:\simon\projects\dashboard-app\data\camera_events.csv'

    return pd.read_csv(data_path)