from flask import Flask, request, jsonify
import cv2
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import csv
from collections import defaultdict
import random
import firebase_admin
from firebase_admin import credentials, firestore
import json


custom_configuration = InferenceConfiguration(confidence_threshold=0.4)
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="zNeRF2bZlwDgvkIf3IUf"
)
app = Flask(__name__)
# Load the data from the CSV file
items = defaultdict(list)
user_items_dict = defaultdict(list)
with open("F:\\MY_PROJECT\\my_data.csv", 'r') as file:
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

def retrive_old(image):
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    # Get a reference to the specific document
    doc_ref = db.collection("in_fridge").document("in_fridge")
    doc = doc_ref.get()
    if doc.exists:
        name = doc.get("name")
        print("Already existing", name)        
    else:
        print("No Existing item found")
        
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

            print("Shelf Life Dictionary:", shelf_life_dict)
            print("Quantity Dictionary:", quantity_dict)
            print("Priority List:", priority_list)
            print("Normal List:", normal_list)
            
            response = {
                'message': 'Success',
                'detected_objects': shelf_life_dict,
                'quantity': quantity_dict,
                'priority_list': priority_list,
                'normal_list': normal_list,
            }
            with open('F:\\Flutter_Test_App\\test\\assets\\recipe.json','w') as json_file:
                json.dump(response,json_file)
            return jsonify(response)

        except Exception as e:
            print(f"Error during object detection: {e}")
            return jsonify({'message': 'Error: Object detection failed'}), 500



@app.route("/generate_recipe", methods=['POST'])
def generate_recipe():
    data = request.json
    priority_list = data.get('priority_list', [])
    normal_list = data.get('normal_list', [])
    csv_file_path = "F:\\MY_PROJECT\\Recipe.csv"
    recipe_data = csv_to_dict(csv_file_path)
    
    if recipe_data is not None:
        try:
            user_ingredients = [priority.strip().lower() for priority in priority_list] + [normal.strip().lower() for normal in normal_list]
            matching_recipes = find_recipe_by_ingredients(user_ingredients, recipe_data)
            
            if matching_recipes:
                shopping_cart = []
                for recipe in matching_recipes[:3]:  # Only consider the first three recipes
                    for ingredient in recipe.get("Ingredients", "").split(','):
                        shopping_cart.append(ingredient.strip().lower())
                
                shopping_cart = list(set(shopping_cart))
                shopping_cart = [item.strip() for item in shopping_cart if item.strip()]
                
                # Randomly select 5 items for recommendation
                num_elements = min(len(shopping_cart), 5)
                recommended_items = random.sample(shopping_cart, num_elements)
                
                response = {
                    'message': 'Success',
                    'recommended_recipes': matching_recipes[:3],  # Return only the first three recipes
                    'shopping_cart_recommendation': shopping_cart,
                    'recommended_items_for_cart': recommended_items
                }
                with open('F:\\Flutter_Test_App\\test\\assets\\recipe.json','w') as json_file:
                    json.dump(response,json_file)
                return jsonify(response)
            else:
                return jsonify({'message': 'No matching recipes found for the given ingredients.'})
        except Exception as e:
            print(f"An unexpected error occurred during processing: {e}")
            return jsonify({'message': 'Error occurred during recipe generation.'}), 500
    else:
        return jsonify({'message': 'Error: Unable to load recipe data.'}), 500


if __name__ == "__main__":
    app.run(debug=False, port=5000)
