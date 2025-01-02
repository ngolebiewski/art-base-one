-- In this SQL file, write (and comment!) the typical SQL queries users will run on your database

-- Add artists to the database. Note, temporarily not using long_bio as it makes output look messy.
INSERT INTO "artists" (
    "first_name", 
    "last_name", 
    "short_bio",
    -- "long_bio",
    "image_url", 
    "birth_country",
    "birth_year",
    "death_year")
VALUES (
    'Pablo',
    'Picasso',
    'Pablo Ruiz Picasso was a Spanish painter, sculptor, printmaker, ceramicist, and theatre designer who spent most of his adult life in France.', -- https://en.wikipedia.org/wiki/Pablo_Picasso
    -- "Pablo Ruiz Picasso (25 October 1881 – 8 April 1973) was a Spanish painter, sculptor, printmaker, ceramicist, and theatre designer who spent most of his adult life in France. One of the most influential artists of the 20th century, he is known for co-founding the Cubist movement, the invention of constructed sculpture,[8][9] the co-invention of collage, and for the wide variety of styles that he helped develop and explore. Among his most famous works are the proto-Cubist Les Demoiselles d'Avignon (1907) and the anti-war painting Guernica (1937), a dramatic portrayal of the bombing of Guernica by German and Italian air forces during the Spanish Civil War.",
    '/images/picasso.png',
    'Spain',
    1881,
    1973
),
    ('Nick', 'Golebiewski', 'Nick Golebiewski is a visual artist and software engineer, with a studio in Brooklyn, NY, who paints images of New York City.', '/images/nick_golebiewski.jpg', 'United States',NULL,NULL)
;

-- add mediums
INSERT INTO "mediums" ("name")
VALUES ('watercolor'), ('oil paint'), ('canvas'), ('paper'), ('pencil'), ('gouache'), ('super 8 film'), ('posca marker'), ('pen & ink');

-- add an artwork
INSERT INTO "artworks" ("artist_id", "title", "size", "year")
VALUES ((SELECT "id" FROM "artists" WHERE "last_name" = "Picasso"), 'The Old Guitarist', '122.9 cm × 82.6 cm', 1903),
    ((SELECT "id" FROM "artists" WHERE "last_name" = "Golebiewski"), 'Grand Street', '2 feet x 3 feet', 2013)        
;

-- add mediums to an artwork
INSERT INTO "artworks_mediums" ("artwork_id", "medium_id")
VALUES(
    (SELECT "id" FROM "artworks" WHERE "title" = 'The Old Guitarist'), 
    (SELECT "id" FROM "mediums" WHERE "name" = "oil paint")
    ),
    (
    (SELECT "id" FROM "artworks" WHERE "title" = 'The Old Guitarist'), 
    (SELECT "id" FROM "mediums" WHERE "name" = "canvas")
    );

-- add another set of mediums to an artwork, would like to find a more efficient way to add, as this is repetitious.
INSERT INTO "artworks_mediums" ("artwork_id", "medium_id")
VALUES(
    (SELECT "id" FROM "artworks" WHERE "title" = 'Grand Street'), 
    (SELECT "id" FROM "mediums" WHERE "name" = "watercolor")
    ),
    (
    (SELECT "id" FROM "artworks" WHERE "title" = 'Grand Street'), 
    (SELECT "id" FROM "mediums" WHERE "name" = "pencil")
    ),
    (
    (SELECT "id" FROM "artworks" WHERE "title" = 'Grand Street'), 
    (SELECT "id" FROM "mediums" WHERE "name" = "paper")
    )
;

-- update an artwork's image url
UPDATE "artworks"
SET "image_url" = '/images/old_guitarist.jpg'
WHERE "title" = 'The Old Guitarist';

-- update another artwork's image url
UPDATE "artworks"
SET "image_url" = '/images/grand-street-gouache.jpg'
WHERE "title" = 'Grand Street';

-- create a series called "Blue Period", info via https://en.wikipedia.org/wiki/Picasso%27s_Blue_Period
INSERT INTO "sections" ("name", "description", "type")
VALUES ("Blue Period", "The Blue Period (Spanish: Período Azul) comprises the works produced by Spanish painter Pablo Picasso between 1901 and 1904. During this time, Picasso painted essentially monochromatic paintings in shades of blue and blue-green, only occasionally warmed by other colors.", "series")
;

-- create another series called "Chinatown"
INSERT INTO "sections" ("name", "description", "type")
VALUES ("Chinatown", "Golebiewski's Chinatown series explores the vibrant neighborhood of NYC in watercolor and gouache, active 2012-present.", "series")
;

-- delete a section if you make a typo!
DELETE FROM "sections" WHERE "name" = 'Chinetown'

-- create a set of departments, which are big umbrellas for artworks.
INSERT INTO "sections" ("name", "description", "type")
VALUES ("Painting", "All forms of painting, including oil, gouache, watercolor, etc.", "department"),
        ("Film", "Video, super 8 film, 16mm, 35mm, and all other moving images", "department"),
        ("Drawing-a-Day", "A daily drawing project", "department")
;

-- update ALL artwork's record to include its department
UPDATE "artworks" 
SET "department" = (SELECT "id" FROM "sections" WHERE "name" = 'Painting');

-- update an artwork's record to include its series.
UPDATE "artworks"
SET "series" = (SELECT "id" FROM "sections" WHERE "name" = 'Blue Period')
WHERE "title" = "The Old Guitarist";

-- again...
UPDATE "artworks"
SET "series" = (SELECT "id" FROM "sections" WHERE "name" = "Chinatown")
WHERE "title" = "Grand Street";

-- Update the price on Nick's painting...
UPDATE "artworks"
set "price" = 3000.00
WHERE "title" = "Grand Street";

-- Now, let's try adding in more fileds at once with some artworks (mediums still need to be added later?)
INSERT INTO "artworks" ("artist_id", "title", "size", "year", "image_url", "department", "series")
VALUES 
    ((SELECT "id" FROM "artists" WHERE "last_name" = "Picasso"), 'Femme aux Bras Croisés (Woman with Folded Arms)', '81 × 58 cm', 1901, 
        '/studio_artist/images/femme_aux_bras_croises.jpg', 
        (SELECT "id" FROM "sections" WHERE "name" = 'Painting'),
        (SELECT "id" FROM "sections" WHERE "name" = 'Blue Period')
        )
;

-- add mediums to an the Femme aux Bras Croisés (Woman with Folded Arms) painting. OUT OF SCOPE: adding mediums when initially creating artwork record.
INSERT INTO "artworks_mediums" ("artwork_id", "medium_id")
VALUES(
    (SELECT "id" FROM "artworks" WHERE "title" = 'Femme aux Bras Croisés (Woman with Folded Arms)'), 
    (SELECT "id" FROM "mediums" WHERE "name" = "oil paint")
    ),
    (
    (SELECT "id" FROM "artworks" WHERE "title" = 'Femme aux Bras Croisés (Woman with Folded Arms)'), 
    (SELECT "id" FROM "mediums" WHERE "name" = "canvas")
    );

-- Search all artworks by artist's last name.
SELECT * FROM "artworks"
WHERE "artist_id" = (SELECT "id" FROM "artists" WHERE "last_name" = "Picasso");

-- Show all human readable artworks by artist's name from the art_list view.
-- i.e. List all of Pable Picasso's artworks in this database.
SELECT * FROM "art_list"
WHERE "name" = "Pablo Picasso";

-- List the mediums used by a specific artwork by its title
SELECT "mediums"."name" AS "medium", "title" 
FROM "mediums"
JOIN "artworks_mediums" ON "mediums"."id" = "artworks_mediums"."medium_id"
JOIN "artworks" ON "artworks_mediums"."artwork_id" = "artworks"."id"
WHERE "artworks_mediums"."artwork_id" = (SELECT "id" FROM "artworks" WHERE "title" = 'The Old Guitarist');

-- List the mediums used by a specific artwork and group together into a list -- note, made this into a view
SELECT GROUP_CONCAT("mediums"."name") AS "mediums", "title", "artworks"."id"
FROM "mediums"
JOIN "artworks_mediums" ON "mediums"."id" = "artworks_mediums"."medium_id"
JOIN "artworks" ON "artworks_mediums"."artwork_id" = "artworks"."id"
WHERE "artworks_mediums"."artwork_id" = (SELECT "id" FROM "artworks" WHERE "title" = 'The Old Guitarist')
GROUP BY "title";

-- Find artwork by portion of an artwork's title, list basic info and artist name
SELECT "title", "size", "year", "first_name", "last_name"
FROM "artworks"
JOIN "artists" on "artists"."id" = "artworks"."artist_id"
WHERE "title" LIKE "%old%"
ORDER BY "title" ASC;

-- How many artworks do each artist have?
SELECT first_name || ' ' || last_name AS "artist", COUNT ("title") as "number artworks"
FROM "artists"
JOIN "artworks" ON "artists"."id" = "artworks"."artist_id"
GROUP BY "artist_id"
ORDER BY "last_name";

-- Which artworks have oil paint as a medium?
SELECT "name" AS "artist", "title", "mediums"
FROM "art_list" 
WHERE "mediums" LIKE "%oil%"
ORDER BY "title" ASC;

-- List all dead artists
SELECT "first_name", "last_name", "death_year", 'deceased'
FROM "artists"
WHERE "death_year" IS NOT NULL;

-- List all artists that are still alive
SELECT "first_name", "last_name", 'alive'
FROM "artists"
WHERE "death_year" IS NULL;

-- We need someone who works at the Met Museum to buy one of Nick's Artworks!
-- First Create the Organization record, since we'll need to attach the org id to the person record...
INSERT INTO "organizations" ("name", "city", "state", "type")
VALUES('Met Museum', 'New York', 'NY', 'museum');

-- Create a person record...
INSERT INTO "persons" ("first_name", "last_name", "org", "type")
VALUES('Hermione', 'Granger', (SELECT "id" FROM "organizations" WHERE "name" = 'Met Museum'), 'curator');

-- Create a sale! Hermione Granger from Hogwarts, I mean, the Met Museum purchase's Nick's Grand Street Painting.
    -- Should be a constraint that the painting cannot already be sold, before selling it (although good for the artist's finances, just is impossible with one of a kind art)
    -- Add to the sold_paintings list and Trigger an update on the sold status of the painting
BEGIN TRANSACTION;
INSERT INTO "sold_artworks" ("artwork_id", "person_id", "org_id", "price", "date_sold")
    VALUES(
        (SELECT "id" FROM "artworks" WHERE "title" = "Grand Street"),
        (SELECT "id" FROM "persons" WHERE "first_name" = 'Hermione' AND "last_name" = 'Granger'),
        (SELECT "id" FROM "organizations" WHERE "name" is "Met Museum"),
        (SELECT "price" FROM "artworks" WHERE "title" = "Grand Street" AND "sold" = 0),  -- checks to make sure artwork isn't already sold
        '2024-12-25'
    );
COMMIT;

-- CHECK the sale record, and then the sold status 
SELECT * FROM "sold_artworks";
SELECT "title", "sold" FROM "artworks" WHERE "sold" = 1;

-- MADE A MISTAKE?
UPDATE "artworks" SET "sold" = 0 WHERE "title" = 'Grand Street';
DELETE FROM "sold_artworks" WHERE "artwork_id" = (SELECT "id" FROM "artworks" WHERE "title" = "Grand Street");

-- OTHER POSSIBLE QUERIES OUTSIDE THE SCOPE OF EXAMPLES FOR COMPLETING THIS PROJECT
    -- Find all artworks in a series
    -- List all series by an artist
    -- Find all artworks within a specific department in a section.
    -- Search artworks by a keyword in descriptions using LIKE
    -- Find all artworks missing an image
    -- Get Sales records by year, month, artist, etc.
