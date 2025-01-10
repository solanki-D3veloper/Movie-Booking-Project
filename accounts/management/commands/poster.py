import os
import requests
from imdb import IMDb

def get_movie_poster_from_imdb(movie_name):
    ia = IMDb()
    movies = ia.search_movie(movie_name)
    
    if movies:
        movie = movies[0]  # Take the first result
        ia.update(movie)  # Fetch more details
        poster_url = movie.get('full-size cover url', None)
        return poster_url
    else:
        return None

def download_poster(poster_url, file_name):
    response = requests.get(poster_url)
    if response.status_code == 200:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download poster for {file_name}")

def download_posters_for_movies(movie_list):
    for movie_name in movie_list:
        print(f"Processing: {movie_name}")
        poster_url = get_movie_poster_from_imdb(movie_name)
        if poster_url:
            # Generate the filename from the movie name (ensure valid filename)
            file_name = f"media/movies/poster/{movie_name.replace(' ', '_').lower()}_poster.jpg"
            download_poster(poster_url, file_name)
        else:
            print(f"Poster not found for {movie_name}")

# List of movie names
movie_list = [
    'The Dark Knight',
    'Inception',
    'The Shawshank Redemption',
    'Forrest Gump',
    'The Matrix'
]

# Download posters for all movies in the list
download_posters_for_movies(movie_list)
