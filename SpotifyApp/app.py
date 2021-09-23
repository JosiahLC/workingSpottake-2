'''Song_Suggester app logic'''
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pickle
import joblib
import lzma
DB = SQLAlchemy()

class Song(DB.Model):
    """Each row is a song and its spotify audio features"""
    __tablename__ = 'song'

    id = DB.Column(DB.String(25), primary_key=True) # Spotify ID for track
    song_name = DB.Column(DB.String(), nullable=False)
    artist_name = DB.Column(DB.String(), nullable=False)
    danceability = DB.Column(DB.Float)
    energy = DB.Column(DB.Float)
    key = DB.Column(DB.Integer)
    loudness = DB.Column(DB.Float)
    mode = DB.Column(DB.Integer)
    speechiness = DB.Column(DB.Float)
    acousticness = DB.Column(DB.Float)
    instrumentalness = DB.Column(DB.Float)
    liveness = DB.Column(DB.Float)
    valence = DB.Column(DB.Float)
    tempo = DB.Column(DB.Float)
    duration_ms = DB.Column(DB.BigInteger)
    time_signature = DB.Column(DB.Integer)

    def __repr__(self):
        return "<{}>".format(self.song_name)

#loading in pickled KNN model

with lzma.open("model.xz", "rb") as f:
    model = pickle.load(f)
from spotify_client import *
from app import *
from wrangle import *
import lzma
import pickle



"""Create and configure an instance of the flask application"""
app = Flask(__name__)



# configure app
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize database
DB.init_app(app)

# create table(s)
with app.app_context():
    DB.create_all()

# ROOT ROUTE
@app.route('/', methods=["GET", "POST"])
def root():     
    """Base view"""
    resp = None
    # When visitor types song and artist then hits a button...
    if request.method == "POST":
        song_name = request.form["song_name"]
        artist_name = request.form["artist_name"]

        # #suggestions happen here; start by retrieving ids of similar tracks
        # spotify_ids = suggest_ids(song_name, artist_name, orig_df, scaled_df) 
        # tracks=DB.session.query(Song).filter(Song.id.in_(spotify_ids)).all()
        # top_hits = tracks[:20]

        # get genres for a simple plot
        # genre_list = relevant_genres(tracks)
        # genre_series = pd.Series(genre_list)
        """with regex, anything rock could be grouped together, anything pop could be grouped together, etc.; then the resulting genre_series.value_counts() could be plotted in a horizontal bar chart -- or at least the biggest few categories could be -- with value_counts().index as tick labels"""
        # plot = genre_series.hist()
        """it would be cool if a button press would display the next closest set.  It would be cooler if matplotlib displayed a 3D plot, with 3 drop-down menus for choosing any 3 features (of 13) for plot axes (or a 3D tSNE plot, not with audio features but with projections to abstract 3D space); and if the color of input song were bright color, similar to neighbors displayed in table, but different from the faded grey others"""

        # return render_template('predict.html',title='home',top_hits= top_hits)

        w = Wrangler()
        orig_df = w.wrangle(raw_df)
        scaled_df = w.transform(orig_df)

        with lzma.open("model.xz", "rb") as f:
            model = pickle.load(f)

        # song = request.values['song_name']
        # artist = request.values['artist_name']


        output = generate_output(song_name, artist_name, orig_df, scaled_df, model)
        print(output)

        return render_template('predict.html', title = 'home', top_hits = output) # might need to change format of output - needs a list (was top_hits = [])
    else: 
        return render_template('predict.html', title = 'home', top_hits = [])

if __name__ == "__main__":
    application.run()
