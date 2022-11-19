from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

def recreate_database(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def load_data():
    data_path = '/workspaces/dashboard-app/data/camera_events.csv'

    return pd.read_csv(data_path)

class CameraEvent(Base):
    __tablename__ = "camera-events"
    id = Column(Integer, primary_key=True)
    number_plate = Column(String)
    created_at = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

engine = create_engine('postgresql+psycopg2://postgres:toothpick@host.docker.internal:5432/metagrated-dev', echo=True)

recreate_database(engine)

Session = sessionmaker(bind=engine)
s = Session()

df = load_data()

for ind in df.index:
    camera_event = CameraEvent(
        number_plate = df['number_plate'][ind],
        created_at = df['created_at'][ind],
        latitude = df['latitude'][ind],
        longitude = df['longitude'][ind]
        )
    s.add(camera_event)

s.commit()

s.close()
