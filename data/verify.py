import csv

positions = set()
duplicates = 0
rows = 0

with open("positions.csv", newline="") as file:
    for row in csv.DictReader(file):
        rows += 1

        fen = row["fen"]
        int(row["evaluation"])

        if fen in positions:
            duplicates += 1

        positions.add(fen)

print("Total rows:", rows)
print("Unique positions:", len(positions))
print("Duplicates:", duplicates)