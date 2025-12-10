import csv

# these are the indices within the list for each row of the airport temperature CSV file
from csv_temperature_indices import MAX_TEMP, MIN_TEMP, YEAR

data_col_years: list[float] = []
data_col_max_temps: list[float] = []
data_col_min_temps: list[float] = []


def make_new_airport_temperature_file(filename1: str, filename2:str):
    """read the data from the given filename, and populate the appropriate lists"""

    fh1 = open(filename1, "r")
    line = fh1.readline()
    fh2 = open(filename2,"w")
    fh2.write(line)

    csv_fh1 = csv.reader(fh1)
    csv_fh2 = csv.writer(fh2, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in csv_fh1:
        if int(line[YEAR]) >= 2000:
            csv_fh2.writerow(line)

if __name__ == "__main__":
    make_new_airport_temperature_file("mtl_airport_temperature.csv", "test_temperatures.csv")
