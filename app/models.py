from datetime import datetime, UTC
from typing import List
from typing import Optional
from sqlalchemy import DateTime, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from .extensions import db


def get_utc_now():
    return datetime.now(UTC)


class Area(db.Model):
    __tablename__ = 'area'
    area_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    local_authority_name: Mapped[str] = mapped_column(String(32))
    local_authority_code: Mapped[str] = mapped_column(String(16))
    lsoa_code: Mapped[str] = mapped_column(String(16))
    geometry: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f'Area(area_id={self.area_id}, local_authority_name={self.local_authority_name}, local_authority_code={self.local_authority_code}, lsoa_code={self.lsoa_code}, geometry={self.geometry})'


class Hours(db.Model):
    __tablename__ = 'hours'
    census_year: Mapped[int] = mapped_column(Integer, primary_key=True)
    lsoa_code: Mapped[str] = mapped_column(String(16), primary_key=True)
    local_authority_name: Mapped[str] = mapped_column(String(32))
    local_authority_code: Mapped[str] = mapped_column(String(16))
    employed_residents: Mapped[int]
    less_than_15: Mapped[int]
    between_16_and_30: Mapped[int]
    between_31_and_48: Mapped[int]
    more_than_48: Mapped[int]
    geometry: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f'Hours(census_year={self.census_year}, lsoa_code={self.lsoa_code}, local_authority_name={self.local_authority_name}, local_authority_code={self.local_authority_code}, employed_residents={self.employed_residents}, geometry={self.geometry})'


class TravelMethod(db.Model):
    __tablename__ = 'travel_method'
    census_year: Mapped[int] = mapped_column(Integer, primary_key=True)
    lsoa_code: Mapped[str] = mapped_column(String(16), primary_key=True)
    local_authority_name: Mapped[str] = mapped_column(String(32))
    local_authority_code: Mapped[str] = mapped_column(String(16))
    employed_residents: Mapped[int]
    work_from_home: Mapped[int]
    underground: Mapped[int]
    train: Mapped[int]
    bus: Mapped[int]
    taxi: Mapped[int]
    motorcycle: Mapped[int]
    car_driver: Mapped[int]
    car_passenger: Mapped[int]
    bicycle: Mapped[int]
    walk: Mapped[int]
    other: Mapped[int]
    geometry: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f'TravelMethod(census_year={self.census_year}, lsoa_code={self.lsoa_code}, local_authority_name={self.local_authority_name}, local_authority_code={self.local_authority_code}, employed_residents={self.employed_residents}, geometry={self.geometry})'


class TravelDistance(db.Model):
    __tablename__ = 'travel_distance'
    census_year: Mapped[int] = mapped_column(Integer, primary_key=True)
    lsoa_code: Mapped[str] = mapped_column(String(16), primary_key=True)
    local_authority_name: Mapped[str] = mapped_column(String(32))
    local_authority_code: Mapped[str] = mapped_column(String(16))
    employed_residents: Mapped[int]
    less_than_2: Mapped[int]
    between_3_and_5: Mapped[int]
    between_6_and_10: Mapped[int]
    between_11_and_20: Mapped[int]
    between_21_and_30: Mapped[int]
    between_31_and_40: Mapped[int]
    between_41_and_60: Mapped[int]
    more_than_60: Mapped[int]
    work_from_home: Mapped[int]
    other: Mapped[int]
    geometry: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f'TravelDistance(census_year={self.census_year}, lsoa_code={self.lsoa_code}, local_authority_name={self.local_authority_name}, local_authority_code={self.local_authority_code}, employed_residents={self.employed_residents}, geometry={self.geometry})'


class Map(db.Model):
    __tablename__ = 'map'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='maps')
    name: Mapped[str] = mapped_column(String(32), default='Untitled Map')
    data: Mapped[str] = mapped_column(String(64000))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now)

    def __repr__(self) -> str:
        return f'Map(id={self.id}, user_id={self.user_id}, name={self.name}, data={self.data}, updated_at={self.updated_at})'


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    occupation: Mapped[Optional[str]] = mapped_column(String(50))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=get_utc_now)
    maps: Mapped[List['Map']] = relationship(back_populates='user', cascade='all,delete-orphan')  # delete orphan maps when user is deleted

    def __repr__(self) -> str:
        return f'User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email_address={self.email_address}, is_email_verified={self.is_email_verified}'
