original_list = {"detected_objects": ["Fresh_tomato 0.30", "Stale_carrot 0.17", "Brinjal 0.75", "Cabbage 0.80"], "message": "Success"}
detected_objects = original_list["detected_objects"]
shelf_life_dict = {}
priority_list = []
normal_list = []

for item in detected_objects:
    # Splitting the detected item and confidence value
    item_name, confidence = item.split()
    confidence = float(confidence)
    updated_item_name = item_name.split('_')[1] if '_' in item_name else item_name
    # Determine shelf life based on item type
    shelf_life = None
    if updated_item_name in ['Brinjal', 'Cabbage']:
        shelf_life = 6  # Usual shelf life under refrigerator for items like Brinjal or Cabbage
    else:
        if 'Fresh' in item_name:
            shelf_life = int(10 * confidence)
        elif 'Stale' in item_name:
            shelf_life = int(10 - 10 * confidence)
            # Since it's already stale, add it directly to the priority list
            priority_list.append(updated_item_name)
    shelf_life_dict[updated_item_name] = shelf_life

# Add items to normal list that are not already stale
for item, shelf_life in shelf_life_dict.items():
    if shelf_life is not None and shelf_life <= 2:
        priority_list.append(item)
    elif shelf_life is not None and shelf_life > 2 and item not in priority_list:  # Avoid duplicates
        normal_list.append(item)

print("Shelf Life Dictionary:", shelf_life_dict)
print("Priority List:", priority_list)
print("Normal List:", normal_list)
