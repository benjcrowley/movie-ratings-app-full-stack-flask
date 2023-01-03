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

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, port=8050)
