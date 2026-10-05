"""Join listing tables and write one row of review/room/price summaries."""
import argparse
from pathlib import Path
import pandas as pd
from exercise_utils import ROOT, read_table


def summarize(price, room, review):
    listings = price.merge(room, on='listing_id', validate='one_to_one').merge(review, on='listing_id', validate='one_to_one')
    if listings.empty:
        raise ValueError('The three tables have no shared listing IDs.')
    dates = pd.to_datetime(listings['last_review'], errors='raise')
    prices = pd.to_numeric(listings['price'].astype(str).str.replace(' dollars', '', regex=False).str.strip(), errors='raise')
    if dates.isna().any() or prices.isna().any():
        raise ValueError('Matched listings must have nonmissing prices and review dates.')
    return pd.DataFrame({
        'first_reviewed': [dates.min().strftime('%Y-%m-%d')],
        'last_reviewed': [dates.max().strftime('%Y-%m-%d')],
        'nb_private_rooms': [int(listings['room_type'].str.lower().str.strip().eq('private room').sum())],
        'avg_price': [round(float(prices.mean()), 2)],
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--price', default=ROOT / 'data/airbnb_price.csv')
    parser.add_argument('--rooms', default=ROOT / 'data/airbnb_room_type.xlsx')
    parser.add_argument('--reviews', default=ROOT / 'data/airbnb_last_review.tsv')
    parser.add_argument('--output', default=ROOT / 'output/airbnb_summary.csv')
    args = parser.parse_args()
    try:
        result = summarize(read_table(args.price, ['listing_id', 'price']),
                           read_table(args.rooms, ['listing_id', 'room_type']),
                           read_table(args.reviews, ['listing_id', 'last_review'], sep='\t'))
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(output, index=False)
        print(result.to_string(index=False))
        print(f'Saved {output}')
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
