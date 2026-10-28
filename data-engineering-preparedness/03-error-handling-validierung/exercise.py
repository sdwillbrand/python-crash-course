"""
Aufgabe: Above Average

Wir möchten Zahlen über das Terminal einlesen und den Durchschnitt berechnen.
Danach möchte wir eine Liste von Listen die ÜBER dem Durchschnitt sind zurückgeben.

> 1
> 2
> 5
> 88
> 598
> 57
> q/quit
[598]

1. Zahlen vom Terminal einlesen, in einer while-Schleife
2. Aus den Zahlen, den Durchschnitt mit sum() berechnen
3. Eine neue Liste mittels List-Comprehension mit Zahlen die größer als der Durchschnitt sind
"""

numbers = []

while True:
    user_input = input("> ")
    # 1. Befehl: Beenden des Programms
    if user_input.lower() in "q" or user_input.lower() in "quit":
        break
    try:
        number = float(user_input)
        numbers.append(number)
    except ValueError:
        print("please enter a valid number or q to exit")

average = sum(numbers) / len(numbers)
above_average = [number for number in numbers if number > average]
print(above_average)
