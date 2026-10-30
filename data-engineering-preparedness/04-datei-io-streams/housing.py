# Erstelle eine Funktion load_data,
# die die CSV Datei (housing.csv) einliest und
# das Ergebnis als Liste von Dicts zurückgibt


import csv


# Extract
def load_data(filepath="housing.csv"):
    with open(filepath, "r", encoding="utf-8") as file:
        housing = csv.DictReader(file)
        return list(housing)  # Erstelle explizit eine Liste bzw eine Kopie


# Transform
def transform_data(housings):
    transformed_housings = []

    for housing in housings:
        housing["sqft"] = int(housing["sqft"])
        housing["bedrooms"] = int(housing["bedrooms"])
        housing["bathrooms"] = int(housing["bathrooms"])
        housing["floor"] = int(housing["floor"])
        housing["price_inr"] = int(housing["price_inr"])
        housing["age_years"] = int(housing["age_years"])
        housing["parking"] = bool(int(housing["parking"]))
        housing["sqm"] = sqft_to_sqm(housing["sqft"])
        housing["price_eur"] = inr_to_eur(housing["price_inr"])

        transformed_housings.append(housing)

    return transformed_housings


# m2 = sqft * 0.092903
# Schreibe eine Funktion sqft_to_sqm, die sqft in sqm umrechnet


def sqft_to_sqm(sqft):
    return sqft * 0.092903


# Schreibe eine Währungskonvertierung von INR -> EUR
# 1 INR = 0,0094 Euro


def inr_to_eur(inr):
    return inr * 0.0094


# Load/Report
def main():
    raw_housings = load_data()
    transformed_housings = transform_data(raw_housings)

    print(f"Total housings: {len(transformed_housings)}")

    prices = [housing["price_eur"] for housing in transformed_housings]
    average_housing_price = sum(prices) / len(prices)
    print(f"Average housing price: {average_housing_price}€")


main()
