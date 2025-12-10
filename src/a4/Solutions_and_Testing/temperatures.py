import csv
import math

import matplotlib.pyplot as plt
import numpy as np

# these are the indices within the list for each row of the airport temperature CSV file
from csv_temperature_indices import MAX_TEMP, MIN_TEMP, YEAR

DATA_COLUMN_YEARS: list[float] = []
DATA_COLUMN_MAX_TEMPS: list[float] = []
DATA_COLUMN_MIN_TEMPS: list[float] = []

# DATA_COLUMN_YEARS: list[float] = []
# DATA_COLUMN_MAX_TEMPS: list[float] = []
# DATA_COLUMN_MIN_TEMPS: list[float] = []
HIGH_THRESHOLD = 28
LOW_THRESHOLD = -20


def straight_line_fit(x, y):
    m, b = np.polyfit(x, y, 1)
    minx = min(x)
    maxx = max(x)
    miny = m * minx + b
    maxy = m * maxx + b
    print(f"{m=}, {b=}")
    return [[minx, maxx], [miny, maxy]]


def read_airport_temperatures(filename: str):
    """read the data from the given filename, and populate the appropriate lists"""

    fh = open(filename, "r")
    fh.readline()

    csv_fh = csv.reader(fh)
    for line in csv_fh:
        if line[MAX_TEMP] != "" and line[MIN_TEMP] != "":
            DATA_COLUMN_YEARS.append(float(line[YEAR]))
            DATA_COLUMN_MAX_TEMPS.append(float(line[MAX_TEMP]))
            DATA_COLUMN_MIN_TEMPS.append(float(line[MIN_TEMP]))


def get_list_of_unique_years() -> list:
    """from the list of all years (the years listed in the 'years' column in the CSV file),
    create a list of years, where each year is never repeated"""
    unique_years = []
    for year in DATA_COLUMN_YEARS:
        if year not in unique_years:
            unique_years.append(year)
    return unique_years


def get_extreme_temperatures(this_year, value, check_below=True) -> int:
    """Count how many times the temperature is above/below the given value in the given year"""
    count = 0
    for year, max_temp, min_temp in zip(DATA_COLUMN_YEARS, DATA_COLUMN_MAX_TEMPS, DATA_COLUMN_MIN_TEMPS):
        if check_below:
            if year == this_year and check_below and min_temp < value:
                count += 1
        else:
            if year == this_year and not check_below and max_temp > value:
                count += 1
    return count


def plot():
    #min_temp = -20
    #max_temp = 28
    read_airport_temperatures("test_temperatures.csv")
    years = get_list_of_unique_years()
    temperature_hot_extremes = []
    temperature_cold_extremes = []
    for year in years:
        temperature_cold_extremes.append(- get_extreme_temperatures(year, LOW_THRESHOLD, check_below=True))
        temperature_hot_extremes.append(get_extreme_temperatures(year, HIGH_THRESHOLD, check_below=False))

    max_num = max(*temperature_cold_extremes, *temperature_hot_extremes)
    max_num = int(math.ceil(max_num/10)*10)
    plt.yticks(list(range(-max_num, max_num, 10)), [str(abs(d)) for d in range(-max_num, max_num, 10)])
    plt.title(f"Dorval Airport - Number of days above {HIGH_THRESHOLD}°C and below {LOW_THRESHOLD}°C")
    plt.bar(years, temperature_cold_extremes, color="BLUE", label="Cold")
    plt.bar(years, temperature_hot_extremes, color="RED", label="Hot")
    x,y = straight_line_fit(years, temperature_cold_extremes)
    plt.plot(x,y)
    x,y = straight_line_fit(years, temperature_hot_extremes)
    plt.plot(x,y)
    plt.show()


if __name__ == "__main__":
    plot()