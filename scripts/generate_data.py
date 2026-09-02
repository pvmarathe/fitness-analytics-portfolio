import random
from datetime import date, timedelta

import pandas as pd

# How many days of fake fitness history we want to generate.
# 180 days is roughly 6 months.
NUM_DAYS = 180

# The most recent day in our fake dataset. date.today() asks the
# computer's clock for today's date.
end_date = date.today()

# timedelta represents a *span* of time (here, "180 days"). Subtracting
# it from end_date gives us the first day of our range.
start_date = end_date - timedelta(days=NUM_DAYS)

print("Start date:", start_date)
print("End date:", end_date)

# The kinds of workouts that can happen on a given day, and roughly how
# likely each one is. These numbers are "weights" - bigger number means
# more likely. They don't need to add up to any particular total.
WORKOUT_TYPES = ["Rest", "Run", "Walk", "Strength", "Yoga", "Cycling"]
WORKOUT_WEIGHTS = [30, 25, 20, 15, 10, 5]


def generate_stats(workout_type, day_offset):
    """Make up realistic-ish duration/distance/calories/heart rate
    for one workout, based on its type."""

    # Rest days have no workout stats at all.
    if workout_type == "Rest":
        return {"duration_min": 0, "distance_km": None,
                "calories": 0, "avg_heart_rate": None}

    # A tiny "fitness improves over time" effect: later days (bigger
    # day_offset) get a small speed/endurance boost. This just scales
    # from 1.0 (day 0) up to about 1.15 (day 180) - a 15% improvement
    # over the 6 months, which is realistic for someone building a habit.
    improvement = 1 + (day_offset / NUM_DAYS) * 0.15

    if workout_type == "Run":
        duration = random.randint(20, 60)
        distance = round(duration / 6 * improvement, 2)  # ~10 min/km pace
        calories = round(duration * 10)
        heart_rate = random.randint(140, 175)
    elif workout_type == "Walk":
        duration = random.randint(20, 90)
        distance = round(duration / 12 * improvement, 2)  # ~slow pace
        calories = round(duration * 4)
        heart_rate = random.randint(90, 115)
    elif workout_type == "Cycling":
        duration = random.randint(30, 90)
        distance = round(duration / 3 * improvement, 2)  # faster than running
        calories = round(duration * 8)
        heart_rate = random.randint(120, 160)
    elif workout_type == "Strength":
        duration = random.randint(30, 75)
        distance = None
        calories = round(duration * 6)
        heart_rate = random.randint(110, 140)
    else:  # Yoga
        duration = random.randint(20, 60)
        distance = None
        calories = round(duration * 3)
        heart_rate = random.randint(80, 105)

    return {"duration_min": duration, "distance_km": distance,
            "calories": calories, "avg_heart_rate": heart_rate}


# Build one row of data per day. A dictionary holds the labeled values
# for that row (like a single row in a spreadsheet), and we collect all
# the rows in a list as we go.
rows = []
for day_offset in range(NUM_DAYS):
    current_date = start_date + timedelta(days=day_offset)

    # random.choices picks ONE item from WORKOUT_TYPES, using
    # WORKOUT_WEIGHTS to make some choices more likely than others.
    # It returns a list with one item in it, so we grab that item with [0].
    workout = random.choices(WORKOUT_TYPES, weights=WORKOUT_WEIGHTS)[0]
    stats = generate_stats(workout, day_offset)

    row = {"date": current_date, "workout_type": workout}
    row.update(stats)  # merge the stats dictionary into row
    rows.append(row)

print(rows[:5])

# Turn our list of dictionaries into a DataFrame - pandas' name for a
# table, with rows and named columns. This is the central object we'll
# use for all our analysis in the notebook.
df = pd.DataFrame(rows)

# Save it to a CSV file (a plain-text spreadsheet format). index=False
# means "don't add an extra column numbering the rows" - pandas does
# this by default, but we don't need it saved to the file.
output_path = "data/fitness_data.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")
print(df.head())
