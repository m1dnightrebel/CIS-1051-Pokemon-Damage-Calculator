import csv

class Move:
    def __init__(self, id, name, move_type, kind, power, accuracy, pp):
        self.id = id
        self.name = name
        self.type = move_type
        self.kind = kind
        self.power = int(power) if power and str(power).isdigit() else 0
        self.accuracy = accuracy
        self.pp = int(pp) if pp and str(pp).isdigit() else 0

    def is_valid(self): #for moves like growl, toxic, et cetera
        return self.power > 0

    def __repr__(self): #to string
        return f"{self.name} ({self.type}, {self.kind}, Power: {self.power})"

# Dictionary to store moves by name
moves_by_name = {}

# Load and parse moves from cleaned CSV
with open('Pokemon Moves.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name'] and row['Type'] and row['Kind']:
            move = Move(
                id=row['#'].strip(),
                name=row['Name'].strip(),
                move_type=row['Type'].strip(),
                kind=row['Kind'].strip(),
                power=row['Power'],
                accuracy=row['Accuracy'].strip(),
                pp=row['PP']
            )
            moves_by_name[move.name] = move
