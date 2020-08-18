# Music Scraper
Music Scraper is a Python application that can grab top artists' data (albums, tracks, profile pictures, etc.) and, if needed, store that data in MongoDB database.

## Table of Contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)

## Introduction
Music Scraper is a Python application that can...
1. Web scrape [Billboard's Top 100 Artists chart](https://www.billboard.com/charts/artist-100 "Billboard Artist 100 Chart") for artist names.
2. Get artists' data, albums, and tracks using [Spotify's Web API](https://developer.spotify.com/documentation/web-api/ "Spotify's Web API")
3. Store the "Artists", "Albums", and "Tracks" as documents inside a MongoDB database.
4. Link the "Artists", "Albums", and "Tracks" together, creating a graph of related documents.

I built Music Scraper to use for a personal project called **FanSpot**, a music forum site built for discussion around artists' discographies.

(Note: If you are interested in following the progress on **FanSpot**, see the [Trello board](https://trello.com/b/F906TQB7 "FanSpot Website").)

## Technologies
This project is created with:
* [Python v3.8.3](https://docs.python.org/release/3.8.3/)
* [Requests v2.22.0](https://requests.readthedocs.io/en/master/)
* [BeautifulSoup v4.9.1](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [MongoEngine v0.20.0](http://docs.mongoengine.org/)
* [Spotipy v2.13.0](https://spotipy.readthedocs.io/en/2.13.0/)

## Setup
### For MacOS
1. Clone the repository:
```
# Clone the repo.
git clone git@github.com:justinyum98/music-scraper.git

# Move into the project directory.
cd music-scraper
```
2. Set up a virtual environment:
```
# Create virtual environment.
python3 -m venv .venv

# Activate the virtual environment.
source .venv/bin/activate
```
3. Run the `setup.py` file:
```
# Install all required packages into virtual environment.
python3 -m pip install .
```

### For Windows
1. Clone the repository:
```
# Clone the repo.
git clone git@github.com:justinyum98/music-scraper.git

# Move into the project directory.
cd music-scraper
```
2. Set up a virtual environment:
```
# Create virtual environment.
py -m venv .venv

# Activate the virtual environment.
.\.venv\Scripts\activate
```
3. Run the `setup.py` file:
```
# Install all required packages into virtual environment.
pip install -e .
```
