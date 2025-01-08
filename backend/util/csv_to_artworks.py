import argparse
import sqlite3
import csv
import os
import logging
from datetime import datetime

# python3 csv_to_artworks.py artwork_csv.csv ../db/artbasethree.db

# CSV headers:
# artist_name, title, size, year, end_year, description, keywords, mediums, series, department, image_url, hi_res_url, price, sold

# Generate a timestamp for the log file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = f"artworks_added_{timestamp}.log"

# Set up logging to log the added artworks with a timestamped filename
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect(db_file)
    return conn

def check_and_insert_artist(conn, artist_name):
    """Check if the artist exists, otherwise insert the artist."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM artists WHERE artist_name = ?", (artist_name,))
    artist = cursor.fetchone()

    if artist is None:
        cursor.execute("INSERT INTO artists (artist_name, first_name, last_name, short_bio) VALUES (?, ?, ?, ?)",
                       (artist_name, 'Unknown', 'Unknown', 'No bio available'))
        conn.commit()
        artist_id = cursor.lastrowid
    else:
        artist_id = artist[0]

    return artist_id

def check_and_insert_medium(conn, medium):
    """Check if the medium exists, otherwise insert it."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM mediums WHERE name = ?", (medium,))
    existing_medium = cursor.fetchone()

    if existing_medium is None:
        cursor.execute("INSERT INTO mediums (name) VALUES (?)", (medium,))
        conn.commit()
        medium_id = cursor.lastrowid
    else:
        medium_id = existing_medium[0]

    return medium_id

def check_and_insert_series(conn, artist_id, series_name):
    """Check if the series exists, otherwise insert it."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM series WHERE name = ? AND artist_id = ?", (series_name, artist_id))
    existing_series = cursor.fetchone()

    if existing_series is None:
        cursor.execute("INSERT INTO series (artist_id, name) VALUES (?, ?)", (artist_id, series_name))
        conn.commit()
        series_id = cursor.lastrowid
    else:
        series_id = existing_series[0]

    return series_id

def check_and_insert_department(conn, department_name):
    """Check if the department exists, otherwise insert it."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM departments WHERE name = ?", (department_name,))
    existing_dept = cursor.fetchone()

    if existing_dept is None:
        cursor.execute("INSERT INTO departments (name) VALUES (?)", (department_name,))
        conn.commit()
        department_id = cursor.lastrowid
    else:
        department_id = existing_dept[0]

    return department_id

def check_and_insert_artwork(conn, artist_id, title, size, year, end_year, description, keywords, price, sold, image_url, hi_res_url, series_id, department_id):
    """Check if the artwork exists (by title, year, artist) and insert it if not."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM artworks WHERE title = ? AND year = ? AND artist_id = ?
    """, (title, year, artist_id))
    existing_artwork = cursor.fetchone()

    if existing_artwork is None:
        cursor.execute("""
            INSERT INTO artworks (artist_id, title, size, year, end_year, description, keywords, price, sold, image_url, hi_res_url, series, department) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (artist_id, title, size, year, end_year, description, keywords, price, sold, image_url, hi_res_url, series_id, department_id))
        conn.commit()
        artwork_id = cursor.lastrowid

        # Log the added artwork
        logging.info(f"Added artwork: {title} by {artist_id}")
    else:
        artwork_id = existing_artwork[0]

    return artwork_id

def insert_mediums_for_artwork(conn, artwork_id, mediums):
    """Insert mediums for the artwork."""
    for medium in mediums:
        medium_id = check_and_insert_medium(conn, medium)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO artworks_mediums (artwork_id, medium_id) VALUES (?, ?)
        """, (artwork_id, medium_id))
        conn.commit()

def process_csv_file(csv_file, db_file):
    """Process the CSV file and insert data into the database."""
    conn = create_connection(db_file)

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            artist_name = row['artist_name']
            title = row['title']
            size = row['size']
            year = row['year']
            end_year = row.get('end_year', None)
            description = row['description']
            keywords = row['keywords']
            price = row.get('price', None)
            
            # Convert the sold value to an integer (1 or 0)
            sold = 1 if row.get('sold', '0') == '1' else 0
            
            image_url = row['image_url']
            hi_res_url = row.get('hi_res_url', None)
            mediums = row['mediums'].split(',')  # Assuming it's a comma-separated list
            series_name = row['series']
            department_name = row['department']

            # Insert artist
            artist_id = check_and_insert_artist(conn, artist_name)

            # Insert series
            series_id = check_and_insert_series(conn, artist_id, series_name)

            # Insert department
            department_id = check_and_insert_department(conn, department_name)

            # Insert artwork
            artwork_id = check_and_insert_artwork(conn, artist_id, title, size, year, end_year, description, keywords, price, sold, image_url, hi_res_url, series_id, department_id)

            # Insert mediums for the artwork
            insert_mediums_for_artwork(conn, artwork_id, mediums)

def main():
    parser = argparse.ArgumentParser(description="Insert artworks from CSV into SQLite database.")
    parser.add_argument('csv_file', help="The path to the CSV file.")
    parser.add_argument('db_file', help="The path to the SQLite database file.")
    args = parser.parse_args()

    process_csv_file(args.csv_file, args.db_file)
    print("Artwork processing complete.")

if __name__ == "__main__":
    main()
