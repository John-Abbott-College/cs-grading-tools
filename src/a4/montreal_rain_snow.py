import csv
import math

import matplotlib.pyplot as plt
import numpy as np

# these are the indices within the list for each row of the airport temperature CSV file
from csv_indices import MAX_TEMP, MIN_TEMP, YEAR, TOTAL_SNOW, TOTAL_RAIN

data_col_years: list[float] = []
data_col_max_temps: list[float] = []
data_col_min_temps: list[float] = []


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
        if line[TOTAL_SNOW] != "" and line[TOTAL_RAIN] != "":
            data_col_years.append(float(line[YEAR]))
            data_col_max_temps.append(float(line[TOTAL_SNOW]))
            data_col_min_temps.append(float(line[TOTAL_RAIN]))


def get_list_of_unique_years() -> list:
    """from the list of all years (the years listed in the 'years' column in the CSV file),
    create a list of years, where each year is never repeated"""
    unique_years = []
    for year in data_col_years:
        if year not in unique_years:
            unique_years.append(year)
    return unique_years


def get_extreme_temperature(this_year, value, check_below=True) -> int:
    """Count how many times the temperature is above/below the given value in the given year"""
    count = 0
    for year, max_temp, min_temp in zip(data_col_years, data_col_max_temps, data_col_min_temps):
        if check_below:
            if year == this_year and check_below:
                count += max_temp
        else:
            if year == this_year and not check_below:
                count += min_temp
    return count


def main():
    min_temp = -00
    max_temp = 0
    read_airport_temperatures("mtl_airport_temperature.csv")
    years = get_list_of_unique_years()
    temperature_hot_extremes = []
    temperature_cold_extremes = []
    for year in years:
        temperature_cold_extremes.append(- get_extreme_temperature(year, min_temp, check_below=True))
        temperature_hot_extremes.append(get_extreme_temperature(year, max_temp, check_below=False))

    max_num = max(*temperature_cold_extremes, *temperature_hot_extremes)
    max_num = int(math.ceil(max_num/100)*100)
    plt.yticks(list(range(-max_num, max_num, 100)), [str(abs(d)) for d in range(-max_num, max_num, 100)])
    plt.title(f"Dorval Airport - Total rain in (mm) and total snow in (cm)")
    plt.bar(years, temperature_cold_extremes)
    plt.bar(years, temperature_hot_extremes)
    x,y = straight_line_fit(years, temperature_cold_extremes)
    plt.plot(x,y)
    x,y = straight_line_fit(years, temperature_hot_extremes)
    plt.plot(x,y)
    plt.show()



main()
