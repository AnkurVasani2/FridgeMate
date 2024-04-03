import csv

food_dict = {
    "Puris": "pro", "Boiled Potatoes": "veg", "Chopped Onions": "veg", "Tomato": "veg", "Sev": "pro",
    "Chat Masala": "pro", "Tamarind Chutney": "pro", "Green Chutney": "pro", "Basmati rice": "veg",
    "Mixed vegetables (carrots, peas, beans)": "veg", "Ginger-garlic paste": "pro", "Biryani masala": "pro",
    "Mint leaves": "veg", "Coriander leaves": "veg", "Ghee": "pro", "Cashews": "pro", "Raisins": "pro",
    "Paneer cubes": "pro", "Yogurt": "pro", "Red chili powder": "pro", "Lemon juice": "pro", "Salt": "pro",
    "Onion slices": "veg", "Bell pepper slices": "veg", "Chicken pieces": "pro", "Turmeric powder": "pro",
    "Oil": "pro", "All-purpose flour": "pro", "Cocoa powder": "pro", "Sugar": "pro", "Baking powder": "pro",
    "Baking soda": "pro", "Eggs": "pro", "Milk": "pro", "Vanilla extract": "pro", "Spaghetti": "pro",
    "Ground beef": "pro", "Garlic": "veg", "Tomato sauce": "veg", "Red wine": "pro", "Olive oil": "pro",
    "Oregano": "veg", "Parmesan cheese": "veg", "Mango": "fruits", "Red bell pepper": "veg", "Red onion": "veg",
    "Jalapeno": "veg", "Lime juice": "fruits", "Cilantro": "veg", "Chicken breasts": "pro", "Spinach": "veg",
    "Feta cheese": "veg", "Peppe": "pro", "Mozzarella cheese": "veg", "Fresh basil leaves": "veg",
    "Balsamic glaze": "pro", "Shrimp": "pro", "Linguine": "pro", "Butter": "pro", "White wine": "pro",
    "Parsley": "veg", "Tomato Puree": "veg", "Cream": "pro", "Ginger": "veg", "Cashew Paste": "pro",
    "Kasuri Methi": "pro", "Red Chili Powder": "pro", "Saffron": "pro", "Peanut": "veg", "Dry Red Chili": "veg",
    "Curry Leaves": "veg", "Fenugreek Seeds": "veg", "Jaggery": "pro", "Capsicum": "veg", "Pav": "veg",
    "Chaat Masala": "pro", "Sambar Powder": "pro", "Matki (Moth Beans)": "veg", "Lemon Wedges": "fruits",
    "Besan": "pro", "Semolina (Rava)": "pro", "Flour Tortillas": "pro", "Avocado": "fruits",
    "Barbecue Sauce": "pro", "Dijon Mustard": "pro", "Apple Cider Vinegar": "pro", "Cloves": "veg"
}

# Write data to CSV file
with open('my_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['items', 'categories'])  # Header
    for item, category in food_dict.items():
        writer.writerow([item, category])

print("CSV file created successfully!")
