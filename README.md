# Ravintolat-Alueellasi

Sovelluksen tehtävänä on helpottaa ravintolan valitsemista kiireessä. Haluatko esimerkiksi joku ilta baari reissun jölkeen nopeasti jotain syötävää halvalla? Sovellus auttaa. Vai haluatko hienon korkea tasoisen illallis kokemuksen? Sovellus auttaa myös tässä. Voit luoda oman käyttäjän johon voit tallentaa suosikki paikkasi ja luoda listoja ravintoloista eri tarpeisiin. Lisäksi kaikki käytttäjät voivat lisätä arvosteluita ravintolalle, joko vain tähtien tai tarkempien kommentti arvosteluiden muodossa. 

*********
Pika update tosiaan apin pitäisi tomia ainakin archilla nyt kun sainkin psql toimimaan. Koneelle pitää asentaa psql ja ajaa seuraavat komennot kun database initialazed

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    restaurant VARCHAR(100) NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review TEXT NOT NULL,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Table for users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Update reviews table to link reviews with users
ALTER TABLE reviews
ADD COLUMN user_id INTEGER REFERENCES users(id);

-- Table for storing favorite restaurants
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    restaurant VARCHAR(100) NOT NULL
);


*********************
