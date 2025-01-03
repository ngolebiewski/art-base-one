from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, DateTime
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

# Artists Table
class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    artist_name = Column(String, nullable=True)
    short_bio = Column(Text, nullable=False)
    long_bio = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    birth_country = Column(String, nullable=True)
    birth_year = Column(Integer, nullable=True)
    death_year = Column(Integer, nullable=True)

# Sections Table
class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    web = Column(Integer, nullable=True)
    order = Column(Integer, nullable=True)

    # Define relationships to 'artworks' for both 'department' and 'series'
    department_artworks = relationship("Artwork", foreign_keys="[Artwork.department]", back_populates="department_section")
    series_artworks = relationship("Artwork", foreign_keys="[Artwork.series]", back_populates="series_section")

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
    department = Column(Integer, ForeignKey("sections.id"), nullable=True)
    series = Column(Integer, ForeignKey("sections.id"), nullable=True)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    price = Column(DECIMAL, nullable=True)
    sold = Column(Integer, default=0, nullable=False)

    # Relationships for 'department' and 'series' in the Artwork model
    department_section = relationship("Section", foreign_keys=[department], back_populates="department_artworks")
    series_section = relationship("Section", foreign_keys=[series], back_populates="series_artworks")

    # Relationship to 'artist'
    artist = relationship("Artist", backref="artworks")

    # Relationship to mediums via join table
    mediums = relationship("Medium", secondary="artworks_mediums", backref="artworks")

# Organizations Table
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address_1 = Column(String, nullable=True)
    address_2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, default="United States", nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    type = Column(String, nullable=False)

# Persons Table
class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone = Column(Integer, nullable=True)
    org = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    note = Column(Text, nullable=True)
    type = Column(String, nullable=False, default="contact")

    # Relationship to organization
    organization = relationship("Organization", backref="persons")

# Sold Artworks Table
class SoldArtwork(Base):
    __tablename__ = "sold_artworks"

    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey("artworks.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    price = Column(DECIMAL, nullable=True)
    date_sold = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    artwork = relationship("Artwork", backref="sold_artworks")
    person = relationship("Person", backref="sold_artworks")
    organization = relationship("Organization", backref="sold_artworks")

# Triggers and Views (Postgres, SQLite-specific, etc.)
# You can implement these via SQLAlchemy or handle them directly in the database

# Example of a view creation (though this may need to be executed via a raw SQL statement)
# CREATE VIEW 'mediums_by_artwork' AS SELECT GROUP_CONCAT('mediums'.'name') AS 'mediums', 'title', 'artworks'.'id' FROM 'mediums' JOIN 'artworks_mediums' ON 'mediums'.'id' = 'artworks_mediums'.'medium_id' JOIN 'artworks' ON 'artworks_mediums'.'artwork_id' = 'artworks'.'id' GROUP BY 'title'
