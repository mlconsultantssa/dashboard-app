from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
from tqdm import tqdm
from models import CameraEvent

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

df = load_data()

for ind in tqdm(df.index):
    camera_event = CameraEvent(
        number_plate = df['number_plate'][ind],
        created_at = df['created_at'][ind],
        latitude = df['latitude'][ind],
        longitude = df['longitude'][ind]
        )
    s.add(camera_event)

s.commit()

s.close()
