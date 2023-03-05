import json

with open('/Users/junotsang/Desktop/dev/FYP/dev/FYP-application/app/rm/category.txt') as f:
    data_str = f.read().replace('\n', ',')

# Parse the JSON array
data = json.loads('[' + data_str + ']')

def make_cat():
    category_dict = {}

    for cat in data:
        main_cat_name = cat['main_cat_name_en']
        sub_cat_name = cat['sub_cat_1_name_en']
        sub_cat_2_name = cat['sub_cat_2_name_en']

        if main_cat_name not in list(category_dict.keys()):
            category_dict[main_cat_name] = {}

        if sub_cat_name not in category_dict[main_cat_name]:
            category_dict[main_cat_name][sub_cat_name] = []

        if sub_cat_2_name not in category_dict[main_cat_name][sub_cat_name]:
            category_dict[main_cat_name][sub_cat_name]. append(sub_cat_2_name)

    return category_dict