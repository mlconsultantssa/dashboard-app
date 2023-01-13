from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

Base = declarative_base()

def recreate_database(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def load_data():
    data_path = '/workspaces/dashboard-app/data/camera_events.csv'

    return pd.read_csv(data_path)

engine = create_engine('postgresql+psycopg2://postgres:toothpick@host.docker.internal:5432/metagrated-dev', echo=True)

recreate_database(engine)

Session = sessionmaker(bind=engine)
s = Session()

df = load_data()[['number_plate', 'created_at', 'camera_id', 'latitude', 'longitude']]

df.to_sql('camera-events', engine, if_exists='append', index=False)

s.commit()

s.close()
