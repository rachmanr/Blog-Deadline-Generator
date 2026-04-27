#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
import random
from datetime import datetime, timedelta




# SETTINGS - CHANGE TO SUIT PREFERENCES ------------------------------------------------------------------------------

input_file = "names.csv"                   # Name of file with MacIDs - only one column, no header row
output_file = "assigned_dates.csv"         # Name of file that will be outputted with deadlines

min_gap = 30                               # Minimum number of days between a student's two deadlines in one term
max_per_date = 3                           # Maximum number of students that can have the same deadline

# -------- TERM 1 --------
start_T1 = datetime(2026, 1, 12)           # First possible deadline for Fall term (y/m/d)
end_T1   = datetime(2026, 3, 26)           # Last possible deadline for Fall term (y/m/d)

startRW_T1 = datetime(2026, 2, 17)         # Last possible deadline before reading week/midterms for Fall term (y/m/d)
endRW_T1   = datetime(2026, 2, 25)         # First possible deadline after reading week/midterms for Fall term (y/m/d)

# -------- TERM 2 --------
start_T2 = datetime(2026, 3, 30)           # First possible deadline for Winter term (y/m/d)
end_T2   = datetime(2026, 6, 10)           # Last possible deadline for Winter term (y/m/d)

startRW_T2 = datetime(2026, 5, 18)         # Last possible deadline before reading week/midterms for Witner term (y/m/d)
endRW_T2   = datetime(2026, 5, 22)         # First possible deadline after reading week/midterms for Winter term (y/m/d)




# SCRIPT ------------------------------------------------------------------------------

# Read names
df = pd.read_csv(input_file, header=None)
names = df[0].tolist()
random.shuffle(names) # randomize order to avoid bias
n = len(names)


# Generate valid dates
def generate_dates(start, end, rw_start, rw_end):
    return [
        start + timedelta(days=i)
        for i in range((end - start).days + 1)
        if not (rw_start <= start + timedelta(days=i) <= rw_end)
    ]


# Assign dates to students
def assign_two_dates_balanced(names, all_dates, min_gap, max_per_date):
    n = len(names)

    # capacity tracking
    date_counts = {d: 0 for d in all_dates}

    dateA = [None] * n
    dateB = [None] * n

    # loop through students
    for i, name in enumerate(names):

        # sort dates by how full they are (least used first)
        sorted_dates = sorted(all_dates, key=lambda d: date_counts[d])

        assigned = False

        # try to assign first date
        for d1 in sorted_dates:

            if date_counts[d1] >= max_per_date:
                continue

            # find valid second dates
            valid_d2 = [
                d for d in sorted_dates
                if (d - d1).days >= min_gap and date_counts[d] < max_per_date
            ]

            if not valid_d2:
                continue

            # pick least-used valid d2
            d2 = valid_d2[0]

            dateA[i] = d1
            dateB[i] = d2

            date_counts[d1] += 1
            date_counts[d2] += 1

            assigned = True
            break

        if not assigned:
            raise ValueError(f"Could not assign dates for {name}")

    return dateA, dateB


# Generate date pools
dates_T1 = generate_dates(start_T1, end_T1, startRW_T1, endRW_T1)
dates_T2 = generate_dates(start_T2, end_T2, startRW_T2, endRW_T2)

# Assign dates for each term
t1_d1, t1_d2 = assign_two_dates_balanced(names, dates_T1, min_gap, max_per_date)
t2_d1, t2_d2 = assign_two_dates_balanced(names, dates_T2, min_gap, max_per_date)


# Format output
def fmt(d):
    return d.strftime("%Y-%m-%d")

output_df = pd.DataFrame({
    "MacID": names,
    "Blog Post 1": [fmt(d) for d in t1_d1],
    "Blog Post 2": [fmt(d) for d in t1_d2],
    "Blog Post 3": [fmt(d) for d in t2_d1],
    "Blog Post 4": [fmt(d) for d in t2_d2],
})

output_df = output_df.sort_values(by="MacID").reset_index(drop=True)

# Save
output_df.to_csv(output_file, index=False)

print("Finished! File saved as:", output_file)

