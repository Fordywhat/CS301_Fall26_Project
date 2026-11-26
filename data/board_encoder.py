def encode_board(fen):
    board, turn, castling, en_passant = fen.split()[:4]

    features = [0] * 837
    pieces = "PNBRQKpnbrqk"

    for rank, row in enumerate(reversed(board.split("/"))):
        file = 0

        for piece in row:
            if piece.isdigit():
                file += int(piece)
            else:
                square = rank * 8 + file
                features[pieces.index(piece) * 64 + square] = 1
                file += 1

    features[768] = int(turn == "w")

    for i, right in enumerate("KQkq"):
        features[769 + i] = int(right in castling)

    if en_passant != "-":
        file = ord(en_passant[0]) - ord("a")
        rank = int(en_passant[1]) - 1
        features[773 + rank * 8 + file] = 1

    return features

if __name__ == "__main__":
    import csv

    with open("positions.csv", newline="") as file:
        row = next(csv.DictReader(file))

    features = encode_board(row["fen"])

    print("FEN:", row["fen"])
    print("Number of features:", len(features))
    print("Evaluation:", row["evaluation"])