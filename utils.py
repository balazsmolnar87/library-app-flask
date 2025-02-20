import csv


def check_credentials(username, password):
    with open("credentials.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False
