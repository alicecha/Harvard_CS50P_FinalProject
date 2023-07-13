import csv

"""
Extracts NPS park names and codes and saves them into a list called parks[]
"""

parks = []

with open("parkcodes.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        parks.append({"name": row["Name"].strip().title(), "code": row["Park Code"]})


