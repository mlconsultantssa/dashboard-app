from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CameraEvent(Base):
    __tablename__ = "camera-events"
    id = Column(Integer, primary_key=True)
    number_plate = Column(String)
    created_at = Column(Date)
    camera_id = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String)
