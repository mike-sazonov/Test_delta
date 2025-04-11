import uuid

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, select
from sqlalchemy.orm import relationship
from .database import Base


class ParcelType(Base):
    __tablename__ = 'parcel_types'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)


class Parcel(Base):
    __tablename__ = 'parcels'
    id = Column(String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50))
    weight = Column(Numeric(10, 2))
    type_id = Column(Integer, ForeignKey('parcel_types.id'))
    declared_value_usd = Column(Numeric(10, 2))
    delivery_cost_rub = Column(Numeric(10, 2), nullable=True)
    session_id = Column(String(255))

    type = relationship("ParcelType")