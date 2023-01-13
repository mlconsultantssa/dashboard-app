import pandas as pd
from sqlalchemy import create_engine, func, or_, desc
from sqlalchemy.orm import declarative_base, sessionmaker
from src.db.models import CameraEvent

Base = declarative_base()

class VehicleEventQueryBuilder:
    def __init__(self):
        engine = create_engine('postgresql+psycopg2://postgres:toothpick@host.docker.internal:5432/metagrated-dev', echo=True)
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
        engine = create_engine('postgresql+psycopg2://postgres:toothpick@host.docker.internal:5432/metagrated-dev', echo=True)
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
        engine = create_engine('postgresql+psycopg2://postgres:toothpick@host.docker.internal:5432/metagrated-dev', echo=True)
        session = sessionmaker(bind=engine)()
        camera_event_value_counts = session.query(CameraEvent.number_plate, func.count('*').label('size'))\
            .group_by(CameraEvent.number_plate)\
            .order_by(desc('size'))\
            .all()

        return [i[0] for i in camera_event_value_counts]
