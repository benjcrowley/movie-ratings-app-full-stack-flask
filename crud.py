"""CRUD OPERATIONS"""
from model import db, User, Movie, Rating, connect_to_db

# create User function
def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


# create a Movie function
def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie"""

    movie = Movie(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path,
    )

    return movie
# view all movies
def view_all_movies():
    """View all movies"""

    return Movie.query.all()

# create a Rating function
def create_rating(score, user, movie):
    """Create and return a new rating"""

    rating = Rating(score=score, user=user, movie=movie)

    return rating


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
