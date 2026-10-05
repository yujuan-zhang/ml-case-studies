"""Summarize HHMM crime times, night locations, and victim age groups."""
import argparse
import numpy as np
import pandas as pd
from exercise_utils import ROOT, read_table, write_json


def summarize(crimes):
    times = pd.to_numeric(crimes['TIME OCC'], errors='raise')
    if times.isna().any() or ((times % 1) != 0).any() or not times.between(0, 2359).all() or ((times % 100) > 59).any():
        raise ValueError('TIME OCC must contain valid integer HHMM times (0000–2359).')
    hours = times.astype(int) // 100
    counts = hours.value_counts()
    peak_hour = int(counts[counts == counts.max()].index.min())
    night = crimes[(hours >= 22) | (hours <= 3)]
    locations = night.groupby('AREA NAME').size().sort_index()
    if locations.empty:
        raise ValueError('No night crimes with an area name were found.')
    ages = pd.to_numeric(crimes['Vict Age'], errors='raise')
    labels = ['0-17', '18-25', '26-34', '35-44', '45-54', '55-64', '65+']
    # Match the original exercise: age 0 denotes unknown and is excluded.
    groups = pd.cut(ages, bins=[0, 17, 25, 34, 44, 54, 64, np.inf], labels=labels)
    frequencies = groups.value_counts().reindex(labels, fill_value=0)
    return {'peak_crime_hour': peak_hour,
            'peak_night_crime_location': str(locations.idxmax()),
            'victim_ages': {label: int(frequencies[label]) for label in labels}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default=ROOT / 'crimes.csv')
    parser.add_argument('--output', default=ROOT / 'output/crime_summary.json')
    args = parser.parse_args()
    try:
        write_json(summarize(read_table(args.input, ['TIME OCC', 'AREA NAME', 'Vict Age'])), args.output)
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
