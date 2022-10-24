import pandas as pd
from shapely.geometry import Point
from geopandas import GeoDataFrame
import matplotlib as mpl
import dash_leaflet as dl

class Mapper:
  def __init__(self, events):
    self.events = events.copy()
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
    self.filter_events(lambda x: x['number_plate'] == number_plate)
    return self

  def filter_events_on_start_date(self, start_date):
    self.filter_events(lambda x: x['created_at'] >= start_date)
    return self

  def filter_events_on_end_date(self, end_date):
    self.filter_events(lambda x: x['created_at'] <= end_date)
    return self

  def generate_map(self):
    geometry = [Point(xy) for xy in zip(self.points['longitude'], self.points['latitude'])]
    gdf = GeoDataFrame(self.points, geometry=geometry, crs="epsg:4326") 
    return gdf.explore(color=self.points['color'], marker_kwds=dict(radius=10, fill=True), popup=True)

  def get_markers(self):
    # Create markers from data frame.
    return [dl.CircleMarker(center=[row['latitude'], row['longitude']], radius=row['size_normalised'] * 20, color=row['color'], fillColor=row['color'], fillOpacity=0.8) for i, row in self.points.iterrows()]  