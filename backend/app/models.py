from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    admin = Column(Integer, default=0, nullable=False)
    
    __table_args__ = (
        CheckConstraint('admin IN (0, 1)', name='admin_check'),
    )

# Artists Table
class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, default='Unknown')
    last_name = Column(String, nullable=False, default='Unknown')
    artist_name = Column(String, nullable=True)
    short_bio = Column(Text, nullable=False)
    long_bio = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    birth_country = Column(String, nullable=True)
    birth_year = Column(Integer, nullable=True)
    death_year = Column(Integer, nullable=True)

# Departments Table
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, CheckConstraint("length(description) <= 300"), nullable=True)
    web = Column(Integer, CheckConstraint("web IN (0, 1)"), nullable=True)
    order = Column(Integer, nullable=True)

# Series Table
class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, CheckConstraint("length(description) <= 300"), nullable=True)
    web = Column(Integer, CheckConstraint("web IN (0, 1)"), nullable=True)
    order = Column(Integer, nullable=True)

    artist = relationship("Artist", backref="series")

# Mediums Table
class Medium(Base):
    __tablename__ = "mediums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

# Artworks-Mediums Association Table
class ArtworkMedium(Base):
    __tablename__ = "artworks_mediums"

    artwork_id = Column(Integer, ForeignKey("artworks.id"), primary_key=True)
    medium_id = Column(Integer, ForeignKey("mediums.id"), primary_key=True)

# Artworks Table
class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    title = Column(String, nullable=False)
    size = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)
    hi_res_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    department = Column(Integer, ForeignKey("departments.id"), nullable=True)
    series = Column(Integer, ForeignKey("series.id"), nullable=True)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    price = Column(DECIMAL, nullable=True)
    sold = Column(Integer, default=0, nullable=False)

    artist = relationship("Artist", backref="artworks")
    mediums = relationship("Medium", secondary="artworks_mediums", backref="artworks")
    department_rel = relationship("Department", backref="artworks")
    series_rel = relationship("Series", backref="artworks")
    
    __table_args__ = (
        CheckConstraint('sold IN (0, 1)', name='sold_check'),
    )

# Organizations Table
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address_1 = Column(String, nullable=True)
    address_2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, default='United States', nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    type = Column(String, CheckConstraint("type IN ('museum', 'gallery', 'non-profit', 'restaurant', 'business', 'other')"), nullable=False)

# Persons Table
class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False, default='Unknown')
    email = Column(String, unique=True, nullable=True)
    phone = Column(Integer, nullable=True)
    org = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    note = Column(Text, nullable=True)
    type = Column(String, default='contact', nullable=False)

    organization = relationship("Organization", backref="persons")
    
    __table_args__ = (
        CheckConstraint("type IN ('collector', 'friend', 'artist', 'client', 'curator', 'other')", name='type_check'),
    )

# Sold Artworks Table
class SoldArtwork(Base):
    __tablename__ = "sold_artworks"

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey("artworks.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    price = Column(DECIMAL, nullable=True)
    date_sold = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    artwork = relationship("Artwork", backref="sold_artworks")
    person = relationship("Person", backref="sold_artworks")
    organization = relationship("Organization", backref="sold_artworks")

# Additional Images Table
class AdditionalImage(Base):
    __tablename__ = "additional_images"

    artwork_id = Column(Integer, ForeignKey("artworks.id"), primary_key=True)
    image_url = Column(String, nullable=False)

    artwork = relationship("Artwork", backref="additional_images")
