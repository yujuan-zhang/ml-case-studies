"""Execute all five synthetic examples from a different working directory."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
import tempfile
import time
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=HERE / 'output')
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    with tempfile.TemporaryDirectory() as tmp:
        def run(script, arguments):
            subprocess.run([sys.executable, str(ROOT / script), *map(str, arguments)],
                           cwd=tmp, check=True, timeout=60)
        for name, script in [
            ('netflix', 'DS01-explore Netflix movie.py'),
            ('nobel', 'DS03-Visualizing the history of Nobel Prize Winners.py'),
            ('crime', 'DS07-Analyzing crime in los angeles.py'),
        ]:
            destination = output / f'{name}.json'
            run(script, ['--input', HERE / name / 'example_input.csv', '--output', destination])
            assert json.loads(destination.read_text()) == json.loads((HERE / name / 'expected_output.json').read_text()), name
        assert (output / 'nobel_female_proportion.png').stat().st_size > 0
        room_xlsx = Path(tmp) / 'rooms.xlsx'
        pd.read_csv(HERE / 'airbnb/rooms.csv').to_excel(room_xlsx, index=False)
        destination = output / 'airbnb.csv'
        run('DS08-Exploring Airbnb Market Trends.py', [
            '--price', HERE / 'airbnb/prices.csv', '--rooms', room_xlsx,
            '--reviews', HERE / 'airbnb/reviews.tsv', '--output', destination,
        ])
        pd.testing.assert_frame_equal(pd.read_csv(destination), pd.read_csv(HERE / 'airbnb/expected_output.csv'))
        # The CSV rooms route must produce the same joined result as Excel.
        run('DS08-Exploring Airbnb Market Trends.py', [
            '--price', HERE / 'airbnb/prices.csv', '--rooms', HERE / 'airbnb/rooms.csv',
            '--reviews', HERE / 'airbnb/reviews.tsv', '--output', output / 'airbnb_csv_rooms.csv',
        ])
        pd.testing.assert_frame_equal(pd.read_csv(destination), pd.read_csv(output / 'airbnb_csv_rooms.csv'))
        run('python toolbox.py', ['--input', HERE / 'population/example_input.csv', '--country', 'CEB',
                                  '--output-dir', output / 'population'])
        pd.testing.assert_frame_equal(pd.read_csv(output / 'population/urban_population.csv'),
                                      pd.read_csv(HERE / 'population/expected_output.csv'))
        assert (output / 'population/urban_population.png').stat().st_size > 0
    print(f'PASS: all five examples match their reference results; {time.monotonic() - start:.2f}s')


if __name__ == '__main__':
    main()
