numbers = [1, 5, 3, 7, 1, 2, 7, 9]
# print(sorted(numbers))


def count_a(w):
    count = 0
    for c in w.lower():
        if "a" == c:
            count += 1

    return count


"""
Def vs Lambda

Lambda weniger mächtig als Def, aber flexibel und kürzer
"""


def len_words(w):
    return len(w)


words = ["Ananas", "Apfel", "Ei", "Banane"]
print(sorted(words, key=lambda w: len(w)))
