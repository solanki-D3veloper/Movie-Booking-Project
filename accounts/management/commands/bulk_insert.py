from django.core.management.base import BaseCommand
from accounts.models import Movie  # Replace 'yourapp' with the actual app name

class Command(BaseCommand):
    help = 'Insert movies in bulk into the accounts_movie table'

    def handle(self, *args, **kwargs):
        movie_data = [
            {
                'movie_name': 'Movie 1',
                'movie_trailer': 'https://example.com/trailer1',
                'movie_rdate': '2024-12-01',
                'movie_des': 'Description of Movie 1',
                'movie_rating': 7.8,
                'movie_poster': 'movies/poster/movie1.jpg',
                'movie_genre': 'Action | Adventure',
                'movie_duration': '2hr 30min'
            },
            {
                'movie_name': 'Movie 2',
                'movie_trailer': 'https://example.com/trailer2',
                'movie_rdate': '2024-11-15',
                'movie_des': 'Description of Movie 2',
                'movie_rating': 8.1,
                'movie_poster': 'movies/poster/movie2.jpg',
                'movie_genre': 'Comedy | Drama',
                'movie_duration': '1hr 50min'
            },
            # More movies can be added here
        ]

        movie_instances = [Movie(**data) for data in movie_data]
        Movie.objects.bulk_create(movie_instances)

        self.stdout.write(self.style.SUCCESS('Successfully inserted movies into the database'))
