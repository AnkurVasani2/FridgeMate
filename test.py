import random

# Sample list
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Number of random elements to select
num_elements = 3

# Get random elements from the list
random_elements = random.sample(my_list, num_elements)

# Create different lists to append the random elements
list1 = []
list2 = []

# Append the random elements to different lists
for element in random_elements:
    if random.random() < 0.5:  # Example condition for appending to different lists
        list1.append(element)
    else:
        list2.append(element)

# Print the random elements in different lists
print("Random elements in List 1:", list1)
print("Random elements in List 2:", list2)
