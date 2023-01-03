""" Script to seed database"""
# Seed our database from the movies.json file in the data folder

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()

# use with open to open movies.json from the data folder
with open("data/movies.json") as f:
    movie_data = json.loads(f.read())

# loop over each movie in movie_data and use the arguments in the crud.create_movie function to create a movie object
# create a movie list to store the movie objects
movies_in_db = []

for movie in movie_data:
    title = movie["title"]
    overview = movie["overview"]
    poster_path = movie["poster_path"]
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()

# create 10 users
users_in_db = []
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"
    # use the create_user function to create a user object
    user = crud.create_user(email, password)
    users_in_db.append(user)
    # create 10 ratings for each user
    ratings = []
    for n in range(10):
        score = randint(1, 5)
        movie = choice(movies_in_db)
        rating = crud.create_rating(score, user, movie)
        ratings.append(rating)
    model.db.session.add_all(ratings)
model.db.session.add_all(users_in_db)
model.db.session.commit()
