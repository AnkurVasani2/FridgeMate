from flask import Flask, request, jsonify
import cv2
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import csv
from collections import defaultdict
import random

custom_configuration = InferenceConfiguration(confidence_threshold=0.4)
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="zNeRF2bZlwDgvkIf3IUf"
)
app = Flask(__name__)
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
        print(items)
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

def csv_to_dict(csv_file):
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            data_dict = [row for row in reader]
            return data_dict
    except FileNotFoundError:
        print(f"Error: File not found at '{csv_file}'")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def find_recipe_by_ingredients(ingredients, recipe_data):
    matching_recipes = []

    for row in recipe_data:
        ingredients_list = [ing.strip().lower() for ing in row.get("Ingredients", "").split(',')]
        if all(ingredient.lower() in ingredients_list for ingredient in ingredients):
            matching_recipes.append(row)

    return matching_recipes



def draw_boxes(image, predictions):
    for prediction in predictions:
        x, y, width, height = map(int, [prediction['x'], prediction['y'], prediction['width'], prediction['height']])
        confidence = prediction['confidence']
        class_name = prediction['class']

        # Draw bounding box
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # Add label and confidence level
        text = f'{class_name} {confidence:.2f}'
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

@app.route('/upload', methods=["POST"])
def upload():
    if request.method == "POST":
        imagefile = request.files['image']
        filename = "image.jpeg"  # Save the file with the same name for consistency

        # Save the uploaded image
        imagefile.save(filename)

        try:
            # Infer using the InferenceHTTPClient
            with CLIENT.use_configuration(custom_configuration):
                result = CLIENT.infer(filename, model_id="final_year_final_train/2")

            # Load the image for drawing boxes
            img = cv2.imread(filename)

            # Draw boxes on the image
            draw_boxes(img, result['predictions'])

            shelf_life_dict = {}
            quantity_dict = {}  # Dictionary to store the quantity of each item
            priority_list = []
            normal_list = []
            ingridients=[]

            for prediction in result['predictions']:
                item_name = prediction['class']
                confidence = prediction['confidence']
                updated_item_name = item_name.split('_')[1] if '_' in item_name else item_name
                shelf_life = None

                # Increment the quantity count for each detected item
                if updated_item_name in quantity_dict:
                    quantity_dict[updated_item_name] += 1
                else:
                    quantity_dict[updated_item_name] = 1

                if updated_item_name in ['Brinjal', 'Cabbage']:
                    shelf_life = 6
                else:
                    if 'Fresh' in item_name:
                        shelf_life = int(10 * confidence)
                    elif 'Stale' in item_name:
                        shelf_life = int(10 - 10 * confidence)
                        priority_list.append(updated_item_name)
                shelf_life_dict[updated_item_name] = shelf_life

            for item, shelf_life in shelf_life_dict.items():
                if shelf_life is not None and shelf_life <= 2:
                    priority_list.append(item)
                elif shelf_life is not None and shelf_life > 2 and item not in priority_list:
                    normal_list.append(item)


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

                    else:
                        print("No matching recipes found for the given ingredients.")
                except Exception as e:
                    print(f"An unexpected error occurred during processing: {e}")
            print("Shelf Life Dictionary:", shelf_life_dict)
            print("Quantity Dictionary:", quantity_dict)
            print("Priority List:", priority_list)
            print("Normal List:", normal_list)
            print("Recipes:",matching_recipes)
            user_items = []
            user_items+=list_for_recommendation
            print("Your items:", ", ".join(user_items))
            recommendations = generate_recommendations(user_items)
            print("Recommended items:",recommendations)
            response = {
                'message': 'Success',
                'detected_objects': shelf_life_dict,
                'quantity': quantity_dict,
                'priority_list': priority_list,
                'normal_list': normal_list,
                'recommended_recipes':matching_recipes,
                'shopping_cart_recommendation':shopping_cart,
                'recommended_items_for_cart':recommendations      # remove this comment after you solve het's model
            }
            return jsonify(response)

        except Exception as e:
            print(f"Error during object detection: {e}")
            return jsonify({'message': 'Error: Object detection failed'}), 500

if __name__ == "__main__":
    app.run(debug=False, port=5000)
