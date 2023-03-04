import pandas as pd
import datetime
from sqlalchemy import create_engine, func, or_, desc, cast, DateTime, Time
from sqlalchemy.orm import declarative_base, sessionmaker
from package.db.models import CameraEvent
import package.db.config as config

Base = declarative_base()

class VehicleEventQueryBuilder:
    def __init__(self):
        engine = create_engine(config.CONNECTION_STRING)
        self.session = sessionmaker(bind=engine)()
        self.flist = []
        self.query = self.session.query(CameraEvent.latitude, CameraEvent.longitude, func.count('*'))

    def filter_out_bad_events(self):
        self.flist.append(or_(CameraEvent.latitude > 1, CameraEvent.latitude < 0))
        return self

    def filter_events_on_number_plate(self, number_plates):
        self.flist.append(CameraEvent.number_plate.in_(number_plates))
        return self

    def filter_events_on_start_date(self, start_date):
        self.flist.append(CameraEvent.created_at >= start_date)
        return self

    def filter_events_on_end_date(self, end_date):
        self.flist.append(CameraEvent.created_at <= end_date)
        return self

    def execute(self):
        self.filter_out_bad_events()
        camera_events = self.query\
            .filter(*self.flist)\
            .group_by(CameraEvent.latitude, CameraEvent.longitude)\
            .all()

        self.session.close()

        return pd.DataFrame.from_records(camera_events, columns=['latitude', 'longitude', 'size'])

    def __del__(self):
        self.session.close()

class ClientCameraQueryBuilder:
    def __init__(self):
        engine = create_engine(config.CONNECTION_STRING)
        self.session = sessionmaker(bind=engine)()
        self.flist = []
        self.query = self.session.query(CameraEvent.camera_id, CameraEvent.latitude, CameraEvent.longitude, func.count('*'))

    def filter_out_bad_events(self):
        self.flist.append(or_(CameraEvent.latitude > 1, CameraEvent.latitude < 0))
        return self

    def filter_events_on_clients(self, clients):
        self.flist.append(CameraEvent.camera_id.in_(clients))
        return self

    def filter_events_on_start_date(self, start_date):
        self.flist.append(CameraEvent.created_at >= start_date)
        return self

    def filter_events_on_end_date(self, end_date):
        self.flist.append(CameraEvent.created_at <= end_date)
        return self

    def load_camera_count(self):
        self.filter_out_bad_events()
        camera_event_value_counts = self.session.query().distinct(CameraEvent.latitude, CameraEvent.longitude).count()

        return camera_event_value_counts

    def execute(self):
        self.filter_out_bad_events()
        camera_events = self.query\
            .filter(*self.flist)\
            .group_by(CameraEvent.camera_id, CameraEvent.latitude, CameraEvent.longitude)\
            .all()

        self.session.close()

        return pd.DataFrame.from_records(camera_events, columns=['camera_id', 'latitude', 'longitude', 'size'])

    def __del__(self):
        self.session.close()

def load_distinct_vehicles():
        engine = create_engine(config.CONNECTION_STRING)
        session = sessionmaker(bind=engine)()
        camera_event_value_counts = session.query(CameraEvent.number_plate, func.count('*').label('size'))\
            .group_by(CameraEvent.number_plate)\
            .order_by(desc('size'))\
            .limit(100)\
            .all()

        return [i[0] for i in camera_event_value_counts]

def load_missing_url_count(client_id):
        engine = create_engine(config.CONNECTION_STRING)
        session = sessionmaker(bind=engine)()
        camera_event_value_counts = session.query(func.count(not CameraEvent.image_url), func.count(CameraEvent.image_url))\
            .filter(CameraEvent.camera_id == client_id)\
            .all()

        return camera_event_value_counts[0]

def load_missing_location_count(client_id):
        engine = create_engine(config.CONNECTION_STRING)
        session = sessionmaker(bind=engine)()
        camera_event_value_counts = session.query(func.count(not CameraEvent.latitude), func.count(CameraEvent.latitude))\
            .filter(CameraEvent.camera_id == client_id)\
            .all()

        return camera_event_value_counts[0]

def load_vehicle_histogram_data(latitude, longitude):
        engine = create_engine(config.CONNECTION_STRING)
        session = sessionmaker(bind=engine)()
        result = session.query(func.date_trunc('year', cast(CameraEvent.created_at, DateTime)).label('year'),
            func.date_trunc('month', cast(CameraEvent.created_at, DateTime)).label('month'),
            func.date_trunc('day', cast(CameraEvent.created_at, DateTime)).label('day'),
            func.count('*').label('size'))\
                .filter(CameraEvent.longitude == longitude)\
                .filter(CameraEvent.latitude == latitude)\
                .group_by('year', 'month', 'day')\
                .all()

        return result

def load_daily_vehicle_histogram_data(latitude, longitude):
        engine = create_engine(config.CONNECTION_STRING)
        session = sessionmaker(bind=engine)()
        result = session.query(cast(func.date_trunc('hour', cast(CameraEvent.created_at, DateTime)), Time).label('hour'),
            func.count('*').label('size'))\
                .filter(CameraEvent.longitude == longitude)\
                .filter(CameraEvent.latitude == latitude)\
                .group_by('hour')\
                .all()

        return result

def load_all_events(latitude, longitude, start_date, end_date, number_plates):
        engine = create_engine(config.CONNECTION_STRING)
        session = sessionmaker(bind=engine)()
        queries = []
        if start_date:
            queries.append(CameraEvent.created_at >= start_date)
        if end_date:
            queries.append(CameraEvent.created_at <= end_date)   
        if number_plates:
            queries.append(CameraEvent.number_plate.in_(number_plates))
        result = session.query(CameraEvent.id, CameraEvent.latitude, CameraEvent.longitude, CameraEvent.number_plate)\
                .filter(or_(CameraEvent.longitude == longitude, CameraEvent.longitude == latitude))\
                .filter(or_(CameraEvent.latitude == latitude, CameraEvent.latitude == longitude))\
                .filter(*queries)\
                .all()

        return result

def load_event_trail_data(number_plate, date):
    engine = create_engine(config.CONNECTION_STRING)
    session = sessionmaker(bind=engine)()
    result = session.query(CameraEvent.created_at, CameraEvent.latitude, CameraEvent.longitude)\
        .filter(or_(CameraEvent.latitude > 1, CameraEvent.latitude < 0))\
        .filter(cast(CameraEvent.created_at, DateTime) >= cast(datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=5), DateTime))\
        .filter(cast(CameraEvent.created_at, DateTime) >= cast(datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=5), DateTime))\
        .filter(CameraEvent.number_plate == number_plate)\
        .order_by(CameraEvent.created_at)\
        .all()

    return pd.DataFrame.from_records(result, columns=['created_at', 'latitude', 'longitude'])
