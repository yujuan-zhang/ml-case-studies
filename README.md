# Data analysis learning exercises

## What it does

This private repository contains personal Python learning exercises. Start with the five standalone examples below: they read tabular data, answer a concrete question, and save a result that can be checked. Other files remain historical notes or unfinished exercises; their status is listed explicitly.

## Input

### Inputs, outputs, and commands

| Exercise | Input contract | Output |
|---|---|---|
| Netflix (DS01) | CSV: `type`, `release_year`, `duration` (numeric minutes), `genre` | JSON: modal 1990s movie duration and count of action movies shorter than 90 minutes |
| Nobel (DS03) | CSV: `year`, `sex`, `birth_country`, `category`, `full_name` | JSON: most common sex/country, highest US-born decade proportion, female-proportion decade/category, first female laureate, repeat names; PNG: female proportions by decade/category |
| Crime (DS07) | CSV: `TIME OCC` (integer HHMM, leading zeros allowed), `AREA NAME`, `Vict Age` | JSON: peak hour, most frequent night location, seven victim-age counts |
| Airbnb (DS08) | Price CSV, room-type CSV or XLSX, review TSV; each has a unique `listing_id`; other fields are `price`, `room_type`, and `last_review` | One-row CSV: `first_reviewed`, `last_reviewed`, `nb_private_rooms`, `avg_price` |
| Population (`python toolbox.py`) | CSV: `CountryCode`, `Total Population`, `Urban population (% of total)`, `Year` | Selected country's CSV with `Total Urban Population`, plus a PNG scatter plot |

```bash
python "DS03-Visualizing the history of Nobel Prize Winners.py" --input examples/nobel/example_input.csv
python "DS07-Analyzing crime in los angeles.py" --input examples/crime/example_input.csv
python "DS08-Exploring Airbnb Market Trends.py" --price examples/airbnb/prices.csv --rooms examples/airbnb/rooms.csv --reviews examples/airbnb/reviews.tsv
python "python toolbox.py" --input examples/population/example_input.csv --country CEB
```

All commands have `--help`. Paths provided on the command line are relative to your current directory; internal defaults and output destinations are resolved beside the scripts. Quote filenames containing spaces. Use `--output` for JSON/CSV summaries or `--output-dir` for population files to avoid overwriting a previous run.

The examples are smoke tests of program behavior, not substantive conclusions about real data. On the synthetic Netflix fixture, the most common numeric duration is used; ties select the smallest duration. Nobel ties select the first sorted group and JSON decade keys are strings. Crime night hours are 22:00–03:59; age 0 follows the original exercise's unknown-age convention and is excluded from age groups. A peak-hour tie selects the earliest hour; a night-location tie selects the first sorted name. Airbnb uses an inner join of all three sources, counts rows rather than distinct row values, and accepts numeric prices or prices ending in ` dollars`. Population counts are truncated to integers as in the original exercise.

The original versions of the five repaired scripts, including alternative answers and personal comments, are preserved verbatim as `.txt` files under `notes/original/`. These notes are not executable entry points.

## Output

JSON summaries, CSV tables and plots in `examples/output/`. Reference files let you check the results.

## Try it

### First working example

Use Python 3.11 in a separate environment, from the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python "DS01-explore Netflix movie.py" --input examples/netflix/example_input.csv
```

Expected result: `duration` is 80 minutes and `short_movie_count` is 2. The program prints these values and writes `output/netflix_summary.json`. The bundled input is deliberately small, synthetic, and unrelated to real Netflix records. Original course datasets are not bundled.

To run and verify all five examples:

```bash
python examples/run_examples.py
# Equivalent shell entry:
bash examples/run_tool.sh
```

The runner executes each exercise from a temporary working directory, compares the generated JSON/CSV to independently specified reference files, checks that the population plot exists, and prints `PASS` only after every comparison succeeds. Outputs go to `examples/output/`. No cloud service, GPU, training weights, or original course dataset is needed.

### Status of the remaining files

| Files | Status and missing prerequisites |
|---|---|
| DS02 and DS04 school scores | Duplicate learning scripts retained. Require the absent `schools.csv`; not verified in this batch. |
| DS09 | Historical duplicate of the original Netflix exercise. Use the verified DS01 entry above. |
| DS06 customer analytics | Existing transformation exercise; requires `customer_train.csv` and has no saved final table. Not verified as a standalone example. |
| `pro1-predictive modelig for agriculture.py` | Existing classification exercise; requires `soil_measures.csv` and a compatible scikit-learn environment. Its older `multi_class` argument is not supported by the current local scikit-learn version. |
| `pro2-Clustering Antarctic Penguin Species.py` | Existing clustering exercise; requires `penguins.csv` and additional scikit-learn dependencies. The original script assumes enough complete rows for its elbow sweep and displays plots interactively. Not verified here. |
| `KMeans.py` | Notebook-style fragment that assumes `model`, `new_points`, and other variables were created elsewhere. Not a standalone program. |
| DS05, DS10, and pro3 market analysis | Empty or comments-only placeholders; no working analysis is claimed. |

`requirements.txt` installs dependencies for the five verified examples only. It does not promise compatibility with the unfinished modeling exercises. No repository license has been selected; original course materials and upstream attribution must be reviewed before any public redistribution.

### Minimal structure

```text
README.md
requirements.txt
<existing exercise filenames>
exercise_utils.py
examples/
  run_examples.py
  run_tool.sh
  <topic>/example_input.csv + expected_output.json or CSV
notes/original/<original script>.txt
.gitignore
```

Each synthetic example has fewer than ten rows. The five-example verification took about 8 seconds with dependencies already available on the local CPU, excluding Python startup and installation. First-run font caching can add time. Performance on full course datasets is not yet measured.

