import pandas as pd

def load_data():
    data_path = '/workspaces/dashboard-app/data/camera_events.csv'

    return pd.read_csv(data_path)

def load_distinct_vehicles():
    data = load_data()
    vehicle_value_counts = data['number_plate'].value_counts().reset_index()

    return vehicle_value_counts['index'].to_list()