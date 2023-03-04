from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import package.db.config as config

Base = declarative_base()

def recreate_database(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def load_data():
    data_path = config.DATA_PATH

    return pd.read_csv(data_path)

engine = create_engine(config.CONNECTION_STRING, echo=True)

recreate_database(engine)

Session = sessionmaker(bind=engine)
s = Session()

df = load_data()[['number_plate', 'created_at', 'camera_id', 'latitude', 'longitude', 'image_url']]

df.to_sql('camera-events', engine, if_exists='append', index=False)

s.commit()

s.close()
