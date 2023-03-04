import pandas as pd
from shapely.geometry import Point
from geopandas import GeoDataFrame
import matplotlib as mpl

def load_data():
    data_path = '/workspaces/dashboard-app/data/camera_events.csv'

    return pd.read_csv(data_path)

def load_distinct_vehicles():
    data = load_data()
    vehicle_value_counts = data['number_plate'].value_counts().reset_index()

    return vehicle_value_counts['index'].to_list()

class VehicleEventQueryBuilder:
    def __init__(self):
        self.events = load_data().copy()
        self.points = pd.DataFrame({'latitude': [], 'longitude': []})

    def clean(self):
        self.events = self.events[(self.events['latitude'] > 1) | (self.events['latitude'] < 0)]
        events_with_neg_longitude = self.events['longitude'] < 0
        self.events.loc[events_with_neg_longitude, ['latitude', 'longitude']] = (self.events.loc[events_with_neg_longitude, ['longitude', 'latitude']].values)
        return self

    def generate_points(self):
        self.points = self.events.groupby(['latitude', 'longitude']).size().to_frame('size').reset_index()
        self.points['color'] = 'blue'
        return self

    def generate_color(self, cmap='plasma'):
        cmap = mpl.cm.get_cmap(cmap)
        self.points['size_normalised'] = (self.points['size'] - self.points['size'].min()) / (self.points['size'].max() - self.points['size'].min())
        self.points['color'] = self.points.apply(lambda x: (mpl.colors.to_hex(cmap(x['size_normalised']))), axis=1)
        return self

    def filter_events(self, filter):
        self.events = self.events[self.events.apply(filter, axis=1)]
        return self

    def filter_events_on_number_plate(self, number_plate):
        self.filter_events(lambda x: x['number_plate'] == number_plate[0])
        return self

    def filter_events_on_start_date(self, start_date):
        self.filter_events(lambda x: x['created_at'] >= start_date)
        return self

    def filter_events_on_end_date(self, end_date):
        self.filter_events(lambda x: x['created_at'] <= end_date)
        return self

    def execute(self):
        return self.points

    def generate_map(self):
        geometry = [Point(xy) for xy in zip(self.points['longitude'], self.points['latitude'])]
        gdf = GeoDataFrame(self.points, geometry=geometry, crs="epsg:4326")
        return gdf.explore(color=self.points['color'], marker_kwds=dict(radius=10, fill=True), popup=True)

