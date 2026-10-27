user = {
    "id": 1,
    "name": "Thomas",
}


def calculate():
    try:
        if 10 / 0:
            print("Rechnung")
    except ZeroDivisionError:
        print("> Null-Division geht nicht.")
    finally:
        # Aufräumen!
        print("Fertig")


print("Vor dem Fehler")

try:
    # print(user["address"])
    print("Im Fehler")

    calculate()

    a = ["Hallo", "Test"]
    print(a[2])  # OutOfBounds

except KeyError as e:
    print("> Key gibt es nicht")
except Exception as e:
    print("> Ich kenne diesen Fehler nicht")

print("Nach dem Fehler")
