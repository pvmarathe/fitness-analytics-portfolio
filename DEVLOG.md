# Dev Log

A running log of progress on this project — what I did, and what I learned.

## Entry 1 — Project setup

- Set up the project folder and a Python virtual environment (an isolated set of packages just for this project)
- Installed Jupyter, pandas, and matplotlib
- Installed and authenticated the GitHub CLI (`gh`)
- Initialized git, added a `.gitignore`, wrote the first `README.md`

Next up: write a script to generate dummy fitness data, then start exploring it in a Jupyter notebook.

## Entry 2 — Dummy data generator

- Wrote `scripts/generate_data.py`, which creates 180 days (~6 months) of simulated workout data: workout type, duration, distance, calories, and average heart rate
- Learned: variables, loops (`for`), lists, dictionaries, functions (`def`), `if/elif/else`, and how pandas turns a list of dictionaries into a `DataFrame` and saves it as a CSV
- Learned about `NaN` — pandas' way of marking missing data (e.g. a Rest day has no distance)
- Built in a small "gradual fitness improvement" trend over the 6 months, to have something real to discover during analysis
- Output saved to `data/fitness_data.csv`
