# Blog Deadline Generator
This script assigns two deadlines per term (4 total) to each student, subject to:

- A minimum gap between a student's deadlines in a single term
- A maximum number of students with a given deadline
- Exclusion of reading week and/or midterm week dates

It outputs a CSV file with the four assigned dates for each student.

## Files
- deadlines.py — main script
- names.csv — input file (one name per row, no header - must be uploaded)
- assigned_dates.csv — output file (generated after running)

## Requirements
- Python 3.x
- pandas

Install required package:
pip install pandas

## How to Run
1. Clone or download this repository
2. Open a terminal (Command Prompt) in the project folder
3. Run python deadlines.py
4. The output will be saved as assigned_dates.csv

## Input Format
names.csv should look like:

<table>
      <tr><td>halla45</td><td> </td></tr>
      <tr><td>oreilly</td><td> </td></tr>
      <tr><td>rachmanr</td><td> </td></tr>
</table>

(No header, one MacID per line)

## Configuration

You can edit these parameters in the script:
- Term start/end dates
- Reading week/midterm periods
- min_gap → minimum days between a student’s two deadlines
- max_per_date → maximum number of students per date

## Constraints

For the script to work, the following must hold (per term):

(number of students × 2) ≤ (number of valid dates × max_per_date)

If this condition is not satisfied, the script may fail. In this case, decrease min_gap or increase max_per_date.

## How It Works

The algorithm:
- Generates valid dates excluding reading week
- Assigns dates in a balanced way (least-used dates first)
- Ensures all constraints are satisfied

## Notes
- Output is sorted alphabetically by MacID
- Input MacIDs are shuffled internally to ensure fair distribution
