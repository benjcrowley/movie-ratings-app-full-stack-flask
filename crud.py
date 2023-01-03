"""CRUD OPERATIONS"""
from model import db, User, Movie, Rating, connect_to_db

# create User function
def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

# view all users
def view_all_users():
    """View all users"""

    return User.query.all()

# get user by email
def get_user_by_id(user_id):
    """Return a user by id."""
    
    return User.query.get(user_id)

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
# get movie by id
def get_movie_by_id(movie_id):
    """Get movie by id"""

    return Movie.query.get(movie_id)

# create a Rating function
def create_rating(score, user, movie):
    """Create and return a new rating"""

    rating = Rating(score=score, user=user, movie=movie)

    return rating


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
