import csv
from collections import defaultdict

# Load the data from the CSV file
items = defaultdict(list)
user_items_dict = defaultdict(list)
with open("F:\MY_PROJECT\my_data.csv", 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        item, category = row['items'].lower(), row['categories']
        if item:
            items[category].append(item)
            user_items_dict[item] = [0] * len(items)

def generate_recommendations(user_items):
    user_categories = set()
    for item in user_items:
        item = item.lower()
        for category, category_items in items.items():
            if item in category_items:
                user_categories.add(category)
                break

    recommendations = []
    for category in user_categories:
        category_items = [item for item in items[category] if item not in user_items]
        recommendations.extend(category_items[:4])

    return recommendations

def main():
    user_items = []
    while True:
        user_input = input("Enter an item (or press Enter to finish): ").strip()
        if not user_input:
            break
        user_items.append(user_input)

    print("Your items:", ", ".join(user_items))
    recommendations = generate_recommendations(user_items)
    print("Recommended items:", ", ".join(recommendations))

    while True:
        generate_more = input("Do you want to generate more recommendations? (y/n) ").lower()
        if generate_more == 'y':
            new_recommendations = generate_recommendations(user_items + recommendations)
            print("New recommended items:", ", ".join(new_recommendations))
            recommendations.extend(new_recommendations)
        else:
            break

if __name__ == '__main__':
    main()