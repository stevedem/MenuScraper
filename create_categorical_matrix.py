# Generates the categorical matrix filled with menu items and their corresponding trigger categories
# Also includes a reference from unique restaurant ID back to the restaurant name and geo-tag
# Author: Steven DeMarco

import os
import csv
import json

categories = []
triggers_csv = []
restaurants = []
rest_names = []

file_names = os.listdir(os.getcwd() + "\menus")

# Retrieves the list of triggers identified in triggers.txt
triggers = [line.rstrip('\n') for line in open("triggers.txt")]

with open('triggers.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        triggers_csv.append(row)

for t in triggers_csv:
    if t[1] not in categories and 'category' not in t[1]:
        categories.append(t[1])

shellfish = []
fish = []
nut = []
peanut = []
dairy = []
egg = []
wheat = []
soy = []

for t in triggers_csv:
    if 'shellfish' == t[1]:
        shellfish.append(t[0])
    elif 'fish' == t[1]:
        fish.append(t[0])
    elif 'nut' == t[1]:
        nut.append(t[0])
    elif 'peanut' == t[1]:
        peanut.append(t[0])
    elif 'dairy' == t[1]:
        dairy.append(t[0])
    elif 'egg' == t[1]:
        egg.append(t[0])
    elif 'wheat' == t[1]:
        wheat.append(t[0])
    elif 'soy' == t[1]:
        soy.append(t[0])
    else:
        continue

unique_id = -1
menu_items_matrix = []


def clean(s):
    """ Cleans string.
    :param s: String
    :return: String
    """
    s = s.replace("&amp;", "&")
    s = s.replace(".", "")
    s = s.replace(",", "")
    s = s.replace("*", "")
    s = s.replace("&", "")
    s = s.replace("-", "")
    s = s.replace("(", "")
    s = s.replace(")", "")
    s = s.replace("$", "")
    return s

# Generates the headers for the first row of the menu_items_cat_matrix.csv file
first_row_matrix = list()
first_row_matrix.append("RestaurantID")
first_row_matrix.append("MenuItem")
for c in categories:
    first_row_matrix.append(c)
menu_items_matrix.append(first_row_matrix)

# Compiles the information from each restaurant's menu into the categorical matrix
for f in file_names:
    hold = f.split(".txt")
    if "_" in hold[0]:
        # Extracts the menu for each restaurant
        menu = [line.rstrip('\n') for line in open("menus\\\\" + f)]

        if menu is not None:
            # Retrieves the information for restaurants.json
            unique_id += 1
            name_geo = hold[0].split("_")
            rest_name = name_geo[0].replace("&amp;", "&")
            rest_geo = name_geo[1]

            rest = dict()
            rest["id"] = unique_id
            rest["name"] = rest_name
            rest_names.append(rest_name)
            rest["geotag"] = rest_geo

            restaurants.append(rest)

            # Process each menu item
            for item in menu:
                if "\t" in item:
                    splits = item.split("\t")
                    if len(splits[1]) < 2:
                        continue
                    else:
                        matrix_row = []
                        cats_for_item = []

                        item_name = clean(splits[0])
                        item_desc = clean(splits[1])

                        name_splits = item_name.split(" ")
                        item_desc_tokens = item_desc.split(" ")

                        # Add name tokens to the item description to adjust for inconsistencies
                        for name_token in name_splits:
                            clean_token = clean(name_token)
                            if clean_token != "":
                                item_desc_tokens.append(name_token)

                        for token in item_desc_tokens:
                            token = clean(token)

                            if token.lower() in triggers:
                                if token.lower() in shellfish:
                                    if 'shellfish' not in cats_for_item:
                                        cats_for_item.append('shellfish')
                                elif token.lower() in fish:
                                    if 'fish' not in cats_for_item:
                                        cats_for_item.append('fish')
                                elif token.lower() in nut:
                                    if 'nut' not in cats_for_item:
                                        cats_for_item.append('nut')
                                elif token.lower() in peanut:
                                    if 'peanut' not in cats_for_item:
                                        cats_for_item.append('peanut')
                                elif token.lower() in dairy:
                                    if 'dairy' not in cats_for_item:
                                        cats_for_item.append('dairy')
                                elif token.lower() in egg:
                                    if 'egg' not in cats_for_item:
                                        cats_for_item.append('egg')
                                elif token.lower() in wheat:
                                    if 'wheat' not in cats_for_item:
                                        cats_for_item.append('wheat')
                                elif token.lower() in soy:
                                    if 'soy' not in cats_for_item:
                                        cats_for_item.append('soy')

                        # Set up the matrix output based upon the 8 categories
                        category_tracker = []
                        for c in categories:
                            if c in cats_for_item:
                                category_tracker.append('0')
                            else:
                                category_tracker.append('1')
                        matrix_row.append(unique_id)
                        matrix_row.append(item_name)
                        for m in category_tracker:
                            matrix_row.append(m)

                        menu_items_matrix.append(matrix_row)
        else:
            continue
    else:
        continue

print "Writing restaurant reference file..."
with open('restaurants.json', 'w') as outfile:
    json.dump(restaurants, outfile)

print "Writing menu items matrix..."
with open('menu_items_categorical_matrix.csv', 'wb') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(menu_items_matrix)

print "Wrote " + str(len(rest_names)) + " total restaurants and " + str(len(menu_items_matrix)) + " menu items."
