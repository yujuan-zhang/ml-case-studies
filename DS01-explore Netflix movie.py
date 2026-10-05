"""Summarize numeric movie durations for movies released in the 1990s."""
import argparse
import pandas as pd
from exercise_utils import ROOT, read_table, write_json


def summarize(df):
    movies = df[df['type'].str.lower() == 'movie'].copy()
    movies['release_year'] = pd.to_numeric(movies['release_year'], errors='raise')
    movies['duration'] = pd.to_numeric(movies['duration'], errors='raise')
    movies = movies[movies['release_year'].between(1990, 1999)]
    modes = movies['duration'].mode()
    if modes.empty:
        raise ValueError('No 1990s movies with numeric durations were found.')
    short_action = movies[(movies['duration'] < 90) & movies['genre'].str.contains('Action', case=False, na=False)]
    return {'duration': int(modes.iloc[0]), 'short_movie_count': int(len(short_action))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default=ROOT / 'netflix_data.csv')
    parser.add_argument('--output', default=ROOT / 'output/netflix_summary.json')
    args = parser.parse_args()
    try:
        result = summarize(read_table(args.input, ['type', 'release_year', 'duration', 'genre']))
        write_json(result, args.output)
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
