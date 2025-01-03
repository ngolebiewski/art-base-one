-- Users
CREATE TABLE "users" (
    "id" INTEGER,
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "admin" TEXT DEFAULT(0) CHECK("admin" IN (0,1))
    PRIMARY KEY("id")
);

-- Represent artist entities in this table
CREATE TABLE "artists" (
    "id" INTEGER,
    "first_name" TEXT NOT NULL, -- use 'Unknown' if not known
    "last_name" TEXT NOT NULL, -- use 'Unknown' if not known
    "artist_name" TEXT, -- Optional, only some artists have an "artist_name", like 'Prince'
    "short_bio" TEXT NOT NULL CHECK(length(short_bio) <= 200),
    "long_bio" TEXT, -- Optional, too long for demos, really clouds up the view
    "image_url" TEXT, -- relative link to image URL. Would like to insert as BLOB in a later version.
    "birth_country" TEXT,
    "birth_year" INTEGER, -- leaving personally identifiable data optional, here and below.
    "death_year" INTEGER,
    PRIMARY KEY("id")
);

-- These are the units that art can be organized within.
-- Originally I had a `series` AND a `department` table, but decided to consolidate since the columns were identical
-- and added in the 'type' field to differentiate. 
CREATE TABLE "sections"(
    "id" INTEGER, 
    "name" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL CHECK(length(description) <= 300),
    "type" TEXT NOT NULL CHECK("type" IN('series', 'department')),
    "web" INTEGER CHECK("web" IN (0, 1)),
    "order" INTEGER,
    PRIMARY KEY("id")
);

CREATE TABLE "mediums"(
    "id" INTEGER, 
    "name" TEXT UNIQUE,
    PRIMARY KEY("id")
);

CREATE TABLE "artworks_mediums"(
    "artwork_id" INTEGER NOT NULL,
    "medium_id" INTEGER NOT NULL,
    PRIMARY KEY("artwork_id", "medium_id")
    FOREIGN KEY("artwork_id") REFERENCES "artworks"("id"),
    FOREIGN KEY("medium_id") REFERENCES "mediums"("id")
);

-- The main record of this database, the ARTWORK! 🖼️
CREATE TABLE "artworks" (
    "id" INTEGER,
    "artist_id" INTEGER NOT NULL,
    "title" TEXT NOT NULL,
    "size" TEXT NOT NULL,
     -- mediums of artwork via a join table
    "year" INTEGER,
    "end_year" INTEGER,
    "image_url" TEXT,
    "hi_res_url" TEXT,
    "description" TEXT,
    "keywords" TEXT,
    "department" INTEGER,
    "series" INTEGER,
    "date_added" TIMESTAMP DEFAULT(CURRENT_TIMESTAMP),
    "price" DECIMAL,
    "sold" INTEGER NOT NULL DEFAULT(0) CHECK("sold" IN (0,1)), -- False/0 = not sold, True/1 = sold
    PRIMARY KEY("id"),
    FOREIGN KEY("artist_id") REFERENCES "artists"("id"),
    FOREIGN KEY("department") REFERENCES "section"("id"),
    FOREIGN KEY("series") REFERENCES "section"("id") -- references a different section id, can you do this?
);

CREATE TABLE "organizations" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "address_1" TEXT,
    "address_2" TEXT,
    "city" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "country" TEXT DEFAULT('United States'),
    "phone" TEXT,
    "email" TEXT,
    "type" TEXT NOT NULL CHECK("type" IN ('museum', 'gallery', 'non-profit', 'restaurant', 'business', 'other')),
    PRIMARY KEY("id")
);

-- persons (rather than the more correct 'people') which represents a person (hence, the plural)
CREATE TABLE "persons" (
    "id" INTEGER,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL, -- use 'Unknown' if not known
    "email" TEXT UNIQUE,
    "phone" INTEGER,
    "org" INTEGER,
    "note" TEXT,
    "type" TEXT NOT NULL DEFAULT('contact') CHECK("type" IN ('collector', 'friend', 'artist', 'client', 'curator', 'other')),
    PRIMARY KEY("id"),
    FOREIGN KEY("org") REFERENCES "organizations"("id")
);

-- A table which answers the question, who purchased the artwork?
CREATE TABLE "sold_artworks" (
    "id" INTEGER,
    "artwork_id" INTEGER NOT NULL,
    "person_id" INTEGER NOT NULL,
    "org_id" INTEGER,
    "price" DECIMAL,
    "date_sold" NUMERIC DATE,
    "timestamp" DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id"),
    FOREIGN KEY("artwork_id") REFERENCES "artworks"("id"),
    FOREIGN KEY("person_id") REFERENCES "persons"("id"),
    FOREIGN KEY("org_id") REFERENCES "organizations"("id")
);

-- This trigger will auto update an artworks sold status from 0 (false) to 1 (true) when added to sold_artworks.
CREATE TRIGGER "update_artwork_sold"
AFTER INSERT ON sold_artworks
FOR EACH ROW
BEGIN
    UPDATE "artworks"
    SET "sold" = 1
    WHERE "id" = NEW."artwork_id";
END;

-- CREATE A VIEW WITH ALL INFO PLACED INTO THE ARTWORKS TAB --> mediums, series, artist names

-- It's tedious to query a join table to list the mediums an artwork is made out of, therefore creating this view.
CREATE VIEW "mediums_by_artwork" AS
SELECT GROUP_CONCAT("mediums"."name") AS "mediums", "title", "artworks"."id"
FROM "mediums"
JOIN "artworks_mediums" ON "mediums"."id" = "artworks_mediums"."medium_id"
JOIN "artworks" ON "artworks_mediums"."artwork_id" = "artworks"."id"
GROUP BY "title";

-- Adds name of series and attaches to artwork id
CREATE VIEW "series_by_artwork" AS
SELECT "name", "artworks"."id"
FROM "sections"
JOIN "artworks" ON "artworks"."series"= "sections"."id";

-- Adds name of department and attaches to artwork id
CREATE VIEW "department_by_artwork" AS
SELECT "name", "artworks"."id"
FROM "sections"
JOIN "artworks" ON "artworks"."department"= "sections"."id";

-- An overall view of the artworks for humans to read, filling in the artist name, mediums, series, and department from their id numbers. 
CREATE VIEW "art_list" AS
SELECT "artworks"."id", first_name || ' ' || last_name AS "name", "artworks"."title", "size", "year", "mediums", "artworks"."image_url", "artworks"."description", 
    "series_by_artwork"."name" AS "series", "department_by_artwork"."name" AS "department", "price", "sold"
FROM ARTWORKS
JOIN ARTISTS ON "artists"."id" = "artworks"."artist_id"
JOIN "mediums_by_artwork" ON "mediums_by_artwork"."id" = "artworks"."id"
LEFT JOIN "series_by_artwork" ON "series_by_artwork"."id" = "artworks"."id"
LEFT JOIN "department_by_artwork" ON "department_by_artwork"."id" = "artworks"."id"
ORDER BY "artists"."last_name" ASC, "artworks"."id" ASC
;

-- helps when searching for artist_ids on Artworks
CREATE INDEX "artist_ids" on "artworks" ("artist_id");

-- helps when searching for titles of Artworks, often used when adding mediums to an artwork, or looking for a painting by name.
CREATE INDEX "titles" on "artworks" ("titles");
