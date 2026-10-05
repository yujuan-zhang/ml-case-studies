"""Read a population CSV in chunks and export one country's urban population."""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exercise_utils import ROOT


def plot_pop(filename, country_code, output_dir):
    filename = Path(filename)
    if not filename.is_file():
        raise ValueError(f'Input not found: {filename}. See the README example command.')
    required = ['CountryCode', 'Total Population', 'Urban population (% of total)', 'Year']
    pieces = []
    for chunk in pd.read_csv(filename, chunksize=1000):
        missing = sorted(set(required) - set(chunk.columns))
        if missing:
            raise ValueError('Missing columns: ' + ', '.join(missing))
        selected = chunk.loc[chunk['CountryCode'] == country_code, required].copy()
        if len(selected):
            for column in required[1:]:
                selected[column] = pd.to_numeric(selected[column], errors='raise')
            if selected[required[1:]].isna().any().any():
                raise ValueError('Selected population rows contain missing numeric values.')
            selected['Total Urban Population'] = (selected['Total Population'] * selected['Urban population (% of total)'] / 100).astype(int)
            pieces.append(selected)
    if not pieces:
        raise ValueError(f'No rows were found for CountryCode={country_code}.')
    data = pd.concat(pieces).sort_values('Year')
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    data.to_csv(output / 'urban_population.csv', index=False)
    ax = data.plot(kind='scatter', x='Year', y='Total Urban Population')
    ax.figure.savefig(output / 'urban_population.png', bbox_inches='tight')
    plt.close(ax.figure)
    print(f'Saved {len(data)} rows and a plot in {output}')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default=ROOT / 'ind_pop_data.csv')
    parser.add_argument('--country', default='CEB')
    parser.add_argument('--output-dir', default=ROOT / 'output/population')
    args = parser.parse_args()
    try:
        plot_pop(args.input, args.country, args.output_dir)
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
