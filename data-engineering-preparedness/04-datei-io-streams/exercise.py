import sys
from pathlib import Path

"""
! Wichtig: Standort von wo, das python Programm ausgeführt wird
"""
path = Path("hello.txt")

if not path.exists():
    print("File not found.")
    sys.exit()
else:
    path.touch()

"""
Datei Modis:
a = append: Neuer Inhalt wird der Datei angehangen
r = read:   Inhalt darf NUR gelesen werden
w = write:  Neuer Inhalt ÜBERSCHREIBT die Datei
+ = Mehrere Modis: a+ = a + r
"""
with open(path, "w+", encoding="utf-8") as file:
    file.write("Hello back!")
