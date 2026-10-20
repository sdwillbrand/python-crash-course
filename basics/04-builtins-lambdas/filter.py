# filter Funktion
# filter(Bedingung (lambda), Liste)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# % (Modulo-Operator) berechnet den Rest, der bei einer Division entspringt
# Bespiel: 7 % 2 = 1, weil 1 der Rest ist, der bei 7 / 2 = 3, Rest 1 übrig bleibt


even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)

odd_numbers = list(filter(lambda x: x % 2 == 1, numbers))
print(odd_numbers)

# Erstelle eine neue Liste, nur mit Zahlen größer gleich 7 mit list() und filter()
greater_than_seven = list(filter(lambda x: x >= 7, numbers))
print(greater_than_seven)


Na = ["Adam", "Bertha", "Caesar", "Dominik", "Emil", "Friedrich", "Gabi"]
# Alle Namen ausfiltern, die ein 'i' im Namen haben
# names_without_i = list(filter(lambda name: "i" not in name, names))
# print(names_without_i)

# Alle Namen die länger als 4 sind
x_longer_than_four = list(filter(lambda x: len(x) > 4, Na))
print(x_longer_than_four)
