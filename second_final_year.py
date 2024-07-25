from flask import Flask, request, jsonify
import cv2
import csv
from collections import defaultdict
import random


app = Flask(__name__)

@app.route('/upload', methods=["POST"])
priority_list=[]
normal_list=[]

csv_file_path = "F:\\MY_PROJECT\\Recipe.csv"
recipe_data = csv_to_dict(csv_file_path)
if recipe_data is not None:
    try:
        # user_input = input("Enter ingredients separated by commas: ")
        user_ingredients=[]
        for priority in priority_list:
            user_ingredients.append(priority.strip().lower())
        for normal in normal_list:
            user_ingredients.append(normal.strip().lower())
        print(user_ingredients)
        # user_ingredients = [ingredient.strip().lower() for ingredient in user_input.split(',')]
        matching_recipes = find_recipe_by_ingredients(user_ingredients, recipe_data)
        list_for_recommendation=[]
        shopping_cart=[]
        if matching_recipes:
            shopping_cart=[]
            count = 0  # Counter to limit the number of recipes displayed
            for recipe in matching_recipes:
                formatted_recipe = {f'{key}': f'{value}' for key, value in recipe.items()}
                # print("Keys:",formatted_recipe.keys())
                # print(formatted_recipe)
                count += 1
                if count == 3:  # Display only 3 recipes
                    for i in range(count):
                        for key, value in formatted_recipe.items():
                            if key == "Ingredients":
                                shopping_cart.extend(value.split(","))
                    shopping_cart = list(set(shopping_cart))
                    shopping_cart = [item.strip() for item in shopping_cart if item.strip()]
                    num_elements = 3
                    random_elements = random.sample(shopping_cart, num_elements)
                    for element in random_elements:
                        list_for_recommendation.append(element)
                    print("Shopping_cart ",shopping_cart)
                    print("List for recommndation (5): ",list_for_recommendation)
                    break