import pandas as pd
import matplotlib as mpl

class VehicleEventDataProcessor:
    def __init__(self, camera_events):
        self.events = camera_events

    def fix_bad_coordinates(self):
        events_with_neg_longitude = self.events['longitude'] < 0

        self.events.loc[events_with_neg_longitude, ['latitude', 'longitude']] = (self.events.loc[events_with_neg_longitude, ['longitude', 'latitude']].values)
        return self

    def generate_points(self):
        self.events = self.events.groupby(['latitude', 'longitude']).agg({'latitude': 'first', 'longitude': 'first', 'size': 'sum'})
        self.events['color'] = 'blue'
        self.events['size_normalised'] = (self.events['size'] - self.events['size'].min()) / (self.events['size'].max() - self.events['size'].min())
        self.events['size_normalised'] = self.events['size_normalised'].fillna(1).clip(0.1, 1)
        return self

    # def generate_color(self, cmap='plasma'):
    #     cmap = mpl.cm.get_cmap(cmap)
    #     self.events['size_normalised'] = (self.events['size'] - self.events['size'].min()) / (self.events['size'].max() - self.events['size'].min())
    #     self.events['color'] = self.events.apply(lambda x: (mpl.colors.to_hex(cmap(x['size_normalised']))), axis=1)
    #     return self

class ClientCameraDataProcessor:
    def __init__(self, camera_events):
        self.events = camera_events

    def fix_bad_coordinates(self):
        events_with_neg_longitude = self.events['longitude'] < 0

        self.events.loc[events_with_neg_longitude, ['latitude', 'longitude']] = (self.events.loc[events_with_neg_longitude, ['longitude', 'latitude']].values)
        self.events = self.events.groupby(['latitude', 'longitude']).agg({'camera_id': 'first', 'latitude': 'first', 'longitude': 'first', 'size': 'sum'})
        return self

    def generate_points(self):
        self.events['color'] = 'blue'
        self.events['size_normalised'] = (self.events['size'] - self.events['size'].min()) / (self.events['size'].max() - self.events['size'].min())
        return self

def fix_bad_coordinates(events):
        events_with_neg_longitude = events['longitude'] < 0

        events.loc[events_with_neg_longitude, ['latitude', 'longitude']] = (events.loc[events_with_neg_longitude, ['longitude', 'latitude']].values)
        return events