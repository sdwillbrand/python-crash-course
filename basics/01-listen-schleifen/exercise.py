# class TestLevel2DropShortNames:
#     def test_keeps_only_names_with_at_least_three_characters(self):
#         assert solution.drop_short_names(["Al", "Bo", "Eva", "Jo"]) == ["Eva"]

#     def test_no_short_names_keeps_everything(self):
#         assert solution.drop_short_names(["Ana", "Bremen"]) == ["Ana", "Bremen"]

#     def test_empty_list_returns_empty_list(self):
#         assert solution.drop_short_names([]) == []


def drop_short_names(names: list):
    """Gibt eine NEUE Liste zurueck, die nur Namen mit mindestens 3 Zeichen
    enthaelt.

    BUG: Der Code entfernt Elemente aus `names`, WAEHREND er ueber genau
    diese Liste iteriert (`names.remove(...)` innerhalb von
    `for name in names:`). Das verschiebt die Indizes mitten im Durchlauf
    und fuehrt dazu, dass manche kurzen Namen uebersprungen werden (nie
    geprueft werden) und faelschlich in der Liste bleiben.

    Finde und behebe den Bug, ohne die Funktionssignatur zu aendern. Baue
    dafuer eine NEUE Ergebnisliste auf, statt die Eingabeliste waehrend
    des Durchlaufs zu veraendern.
    """
    result = []
    for name in names:
        # Die Invariante/Bedingung wird invertiert
        if len(name) >= 3:
            # names.remove(name)
            result.append(name)
    return result


names = ["Al", "Bo", "Eva", "Jo"]
# Expected return: ["Eva"]

"""
1. Iteration: name = "Al", index = 0
"Al" wird gelöscht: names = ["Bo", "Eva", "Jo"]

2. Iteration: name = "Eva", index = 1

3. Iteration: name = "Jo", index = 2

"""

print(drop_short_names(names))
