"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "secret"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route("/movies")
def all_movies():
    """View all movies."""

    movies = crud.view_all_movies()

    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a specific movie."""

    movie = crud.get_movie_by_id(movie_id)
    all_ratings = crud.view_all_ratings(movie_id)
    # get the rating from the current user in session
    current_user_rating = None
    if "user_id" in session:
        current_user_rating = crud.get_user_rating(session["user_id"], movie_id)

    # get the average score from all ratings
    total_score = 0
    for rating in all_ratings:
        total_score += rating.score
    if len(all_ratings) > 0:
        average_score = total_score / len(all_ratings)
    print(all_ratings)
    return render_template("movie_details.html", movie=movie, all_ratings=all_ratings, average_score=average_score, current_user_rating=current_user_rating)

# Create a new rating for a movie
@app.route("/movies/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    """Create a new rating for a movie."""

    score = request.form.get("score")
    user_id = session["user_id"]
    movie = crud.get_movie_by_id(movie_id)
    user = crud.get_user_by_id(user_id)

    rating = crud.create_rating(score, user, movie)
    db.session.add(rating)
    db.session.commit()
    flash("Rating added!")

    return redirect(f"/movies/{movie_id}")
# delete a rating
@app.route("/remove_rating/<rating_id>/<movie_id>")
def delete_rating(rating_id, movie_id):
    """Delete a rating."""

    rating = crud.get_rating_by_id(rating_id)
    movie_id = movie_id
    db.session.delete(rating)
    db.session.commit()
    flash("Rating deleted!")

    return redirect(f"/movies/{movie_id}")
    
@app.route("/users")
def all_users():
    """View all users."""

    users = crud.view_all_users()

    return render_template("all_users.html", users=users)

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a specific user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_profile.html", user=user)

# Create a new user
@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("This email is already registered.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

# log in
@app.route("/login" , methods=["POST"])
def login():
    """Log in user."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        if user.password == password:
            session["user_id"] = user.user_id
            flash("Logged in!")
        else:
            flash("Incorrect password.")
    else:
        flash("No account with that email. Please register.")
    
    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, port=8050)
