def double(number):
    return number * 2


double(10)

print(double(10))  # This will print 20

result = double(10)

# lambda
# double2 ist eine Variable die eine Funktion beinhaltet
double = lambda number: number * 2

name = "Test"
age = 10
isChild = True

result = double(15)
print(result)

numbers = [1, 2, 3, 4, 8]

# Aufgabe: Quadriere jede Zahl in der Liste
# number_squared = list(numbers * 2, numbers)

numbers_squared = []
for number in numbers:
    numbers_squared.append(
        number**2  # number * number == number ** 2
    )  # neue Zahlen werden zu der neuen Liste hinzugefügt mittels der append Methode

numbers_squared = list(map(lambda x: x**2, numbers))
# f(x) = x^2 => f(2) = 2^2 = 4
# [x1, x2, x3, x4, x5]
# [1, 2, 3, 4, 8]
# => [f(x1), f(x2), f(x3), f(x4), f(x5)]
# => [f(1), f(2), f(3), f(4), f(8)]
# => [1, 4, 9, 16, 64]


numbers_times_ten = list(map(lambda x: x * 10, numbers))

numbers_negate = list(map(lambda x: -x, numbers))

print(numbers_squared)

names = ["Max", "Stefan", "Fritz"]

names_lowercase = list(map(lambda name: name.lower(), names))
print(names_lowercase)

names_uppercase = list(map(lambda name: name.upper(), names))
print(names_uppercase)
