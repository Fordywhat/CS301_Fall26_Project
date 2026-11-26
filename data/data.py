from datasets import load_dataset
import csv

from itertools import groupby, islice

dataset = load_dataset(
    "Lichess/chess-position-evaluations",
    split="train",
    streaming=True
)

def take_positions(dataset, limit):
    groups = groupby(dataset, key=lambda row: row["fen"])

    for fen, rows in islice(groups, limit):
        yield from rows

positions = {}
last_reported = None

for row in take_positions(dataset, 10000000):
    fen = row["fen"]
    cp = row["cp"]

    if cp is None:
        mate = row["mate"]

        if mate is None:
            continue
        elif mate > 0:
            cp = 30000 - mate
        elif mate < 0:
            cp = -30000 - mate
        else:
            cp = -30000 if fen.split()[1] == "w" else 30000

    score = cp if fen.split()[1] == "w" else -cp
    rank = (row["depth"], row["knodes"], score)

    if fen not in positions or rank > positions[fen][0]:
        positions[fen] = (rank, cp)
    if len(positions) % 10000 == 0 and fen != last_reported:
        print("Unique positions:", len(positions))
        last_reported = fen   

with open("positions_10m.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["fen", "evaluation"])

    for fen, value in positions.items():
        writer.writerow([fen, value[1]])

print("Saved", len(positions), "unique positions.")