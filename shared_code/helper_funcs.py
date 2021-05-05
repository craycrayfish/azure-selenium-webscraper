import csv

def csv_to_dict(path):
    """Creates a dictionary from a given path to a csv file, with the first element of each row being the dict key
    and the second being the value
    """
    output = {}
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            output[row[0]] = row[1]
    return output
