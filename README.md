# Ravintola-arvostelu Web-sovellus

Tämä web-sovellus on Flaskilla, Pythonilla ja PostgreSQL:llä toteutettu alusta, jossa käyttäjät voivat:

- Rekisteröityä ja kirjautua sisään omilla tunnuksillaan.
- Lisätä uusia ravintoloita (nimen ja osoitteen kera), kun he ovat kirjautuneena.
- Tarkastella kaikkia järjestelmään lisättyjä ravintoloita.
- Lisätä arvosteluja ravintoloille (arvosana 1-5 ja vapaaehtoinen teksti) vain kirjautuneena käyttäjänä.
- Katsoa jokaisen ravintolan yhteydessä kyseisen ravintolan arvosteluja ja nähdä, kuka ne on tehnyt.

Sovellus hyödyntää Flask-kirjastoa web-kehykseen, SQLAlchemyä tietokantamallinnukseen ja ORM-toiminnallisuuteen sekä Flask-Login -kirjastoa käyttäjien todennukseen ja istuntokäsittelyyn. Näin SQL-injektiot ja monet muut tietoturvaongelmat minimoidaan. Kirjautumattomat käyttäjät voivat selata ravintoloita ja nähdä arvosteluja, mutta vain kirjautuneet käyttäjät voivat lisätä uusia ravintoloita ja arvosteluja.

## Ominaisuudet

- **Rekisteröityminen ja kirjautuminen:**  
  Käyttäjä voi luoda oman tunnuksen antamalla käyttäjänimen ja salasanan. Salasana tallennetaan hashattuna (ei selväkielisenä). Kirjautumisen jälkeen käyttäjä voi toimia tunnistetusti järjestelmässä.

- **Ravintolan lisääminen:**  
  Kirjautunut käyttäjä voi lisätä järjestelmään ravintolan nimen ja osoitteen. Ravintoloiden nimet ovat yksilöllisiä.

- **Ravintoloiden katselu:**  
  Kaikki käyttäjät voivat selata sovellukseen lisättyjä ravintoloita. Jokaisella ravintolasivulla näkyvät sen arvostelut.

- **Arvostelujen lisääminen:**  
  Kirjautuneet käyttäjät voivat lisätä arvosteluja: asettaa arvosanan 1-5 väliltä ja halutessaan liittää mukaan teksti arvostelun. Arvostelu tallentuu käyttäjän tunnuksella, jotta voidaan nähdä, kuka arvostelun on tehnyt.

- **Tietoturva:**  
  Sovellus hyödyntää:
  - SQLAlchemy ORM:ää, joka estää SQL-injektiot käyttäen parametroiduja kyselyitä.
  - Flask-WTF:n CSRF-suojauksella varustettuja lomakkeita.
  - Salasanojen hashäystä käyttäen werkzeug.security -kirjastoa.

## Teknologiat

- **Backend:** Python (Flask), SQLAlchemy, Flask-Login, Flask-WTF
- **Tietokanta:** PostgreSQL
- **Frontend:** HTML, Bootstrap (CDN:n kautta)

## Asennusohjeet

1. Asenna riippuvuudet:

2. Konfiguroi psql
createdb restaurant_db
psql -U username -d restaurant_db -f schema.sql
Muista päivittää db tiedot env tiedostoon

3. Aja ohjelma
   flask run

