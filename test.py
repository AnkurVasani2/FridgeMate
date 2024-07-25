import csv
import re

unique_ingredients = set()

# Open the CSV file and read each row
with open("Recipe.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Use regular expression to split the ingredients string while ignoring text within parentheses
        ingredients = re.findall(r'\b\w+\b', row["Ingredients"])
        for ingredient in ingredients:
            unique_ingredients.add(ingredient.strip())

# Convert the set to a list
unique_ingredients_list = list(unique_ingredients)

print(unique_ingredients_list)
