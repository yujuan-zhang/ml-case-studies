"""Answer five laureate-table questions and save the results as JSON."""
import argparse
import pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exercise_utils import ROOT, read_table, write_json


def summarize(df):
    df = df.copy()
    df['year'] = pd.to_numeric(df['year'], errors='raise')
    df['decade'] = (df['year'] // 10) * 10
    female = df[df['sex'] == 'Female'].sort_values(['year', 'category'])
    if female.empty or df['birth_country'].mode().empty or df['sex'].mode().empty:
        raise ValueError('The example requires a female laureate and nonmissing sex/country values.')
    usa = df.assign(usa=df['birth_country'].eq('United States of America')).groupby('decade')['usa'].mean()
    proportions = df.assign(female=df['sex'].eq('Female')).groupby(['decade', 'category'])['female'].mean()
    decade, category = proportions.idxmax()
    counts = df['full_name'].value_counts()
    return {
        'top_gender': str(df['sex'].mode().iloc[0]),
        'top_country': str(df['birth_country'].mode().iloc[0]),
        'max_decade_usa': int(usa.idxmax()),
        'max_female_dict': {str(int(decade)): str(category)},
        'first_woman_name': str(female.iloc[0]['full_name']),
        'first_woman_category': str(female.iloc[0]['category']),
        'repeat_list': counts[counts >= 2].index.tolist(),
    }


def save_plot(df, path):
    decades = (pd.to_numeric(df['year'], errors='raise') // 10) * 10
    proportions = df.assign(decade=decades, female=df['sex'].eq('Female')).groupby(['decade', 'category'])['female'].mean()
    fig, ax = plt.subplots()
    for category, values in proportions.groupby(level='category'):
        ax.plot(values.index.get_level_values('decade'), values.values, marker='o', label=category)
    ax.set(xlabel='Decade', ylabel='Proportion of Female Winners', title='Female Nobel Prize Winners Over Time')
    ax.legend()
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {path}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default=ROOT / 'data/nobel.csv')
    parser.add_argument('--output', default=ROOT / 'output/nobel_summary.json')
    args = parser.parse_args()
    try:
        df = read_table(args.input, ['year', 'sex', 'birth_country', 'category', 'full_name'])
        write_json(summarize(df), args.output)
        output = Path(args.output)
        save_plot(df, output.with_name(output.stem + '_female_proportion.png'))
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
