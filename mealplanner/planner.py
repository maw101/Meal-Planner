from dataclasses import dataclass, field
from typing import List
import re
import os
import random
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# get current working directory
CWD = os.getcwd()

@dataclass
class Meal:
    name: str = ''
    category: str = ''
    fileloc: str = ''
    ingredients: List[str] = field(default_factory=list)
    
def get_meal(filepath):
    meal = Meal()
    meal.fileloc = filepath
    ingredients = []
        
    # read file contents from file
    with open(filepath, 'r') as recipe_file:
        searching_for = 'name'
        searching_for_regex = '# (.*)'  # pattern for recipe name
        
        for line in recipe_file:
            if line.isspace():
                continue  # skip
            elif searching_for == 'name':
                search = re.search(searching_for_regex, line)
                # check to see if on the line with the name
                if search is not None:
                    meal.name = search.group(1)
                    searching_for = 'category'
                    searching_for_regex = '(\*\*Meal Category\*\* )(.*)'
            elif searching_for == 'category':
                search = re.search(searching_for_regex, line)
                # check to see if on the line with the category name
                if search is not None:
                    meal.category = search.group(2)
                    searching_for = 'ingredients'
                    searching_for_regex = '## Ingredients'
            elif searching_for == 'ingredients':
                search = re.search(searching_for_regex, line)
                # check to see at start of ingredients section
                if search is not None:
                    searching_for = 'ingredient'
                    searching_for_regex = '## Instructions'
            elif searching_for == 'ingredient':
                search = re.search(searching_for_regex, line)
                # check to see if still inside ingredients section
                if search is None:
                    search = re.search('(.*)', line)
                    ingredients.append(search.group(1))
                else:
                    searching_for = ''
            else:
                break  # finished
        
    meal.ingredients = ingredients
    return meal

def get_meals_from_file():
    recipes_directory = os.path.join(CWD, 'recipes')
    # create dictionary of meals by category
    meals = {}
    
    # get category folder names
    categories = [dI for dI in os.listdir(recipes_directory)]
    
    for category in categories:
        category_directory = os.path.join(recipes_directory, category)
        # add category to the dictionary
        meals[category] = [get_meal(os.path.join(category_directory, file)) for file in os.listdir(category_directory) if os.path.isfile(os.path.join(category_directory, file))]

    return meals

def get_plan_details():
    # get actual categories
    possible_categories = [dI for dI in os.listdir(os.path.join(CWD, 'recipes'))]
    print('\nPossible Categories: ', ', '.join(possible_categories))
    # get users categories
    categories_input = input('Enter categories to include each day from the above list (separate by commas): ')
    categories_input = categories_input.split(',')
    categories_input = [cat.strip().lower().replace(' ', '_') for cat in categories_input]
    # only take valid categories
    categories = [cat for cat in categories_input if cat in possible_categories]
    # number of days
    while True:
        try:
            input_val = int(input('Enter number of days to generate plan for (integer): '))
            number_of_days = input_val
            break
        except ValueError:
            print('Invalid Input, must be an integer value.')
    
    return (number_of_days, categories)

def print_category(all_categories, category_name):
    category = all_categories[category_name]
    # print formatted category name
    print(category_name.replace('_', ' ').title())
    print('-' * (len(category_name) + 2)) # spacer between category and meal
    # print each meal in turn
    for (i, meal) in enumerate(category, start=1):
        print('%d) %s' % (i, meal.name))

def replace_meal(plan, day_number):
    days_meals = list(plan[day_number - 1])
    valid_meal_categories = [meal.category.strip().lower() for meal in days_meals]
    
    print('\nReplacing Meal on Day', day_number, ':')
    
    if len(valid_meal_categories) != 1:
        print('Valid Meal Categories:', ', '.join(valid_meal_categories))
        
        # get the meal category from the user
        while True:
            category = input('Which meal category? ')
            category = category.strip().lower()
            if category in valid_meal_categories:
                break
            else:
                print('Invalid Category Entered')
    
    # if only one category, automatically select it
    else:
        category = valid_meal_categories[0].strip().lower()


    all_categories_meals = get_meals_from_file()
    
    print('\nYour options for the', category, 'replacement:\n')
    
    print_category(all_categories_meals, category)
    
    # get the number of the meal to replace
    while True:
        try:
            meal_number = int(input('Enter number of meal to replace current option with: '))
            
            # check is within our allowed range
            if (meal_number >= 1) and (meal_number <= len(all_categories_meals[category])):
                meal_number -= 1  # convert to zero based index
                break
    
            # not within our allowed range
            else:
                print('Invalid Input, must be a valid number from the meals listed above.')

        # handle case of non-integer input
        except ValueError:
            print('Invalid Input, must be an integer value.')

    # find old meal index
    for index, meal in enumerate(days_meals):
        if meal.category.strip().lower() == category:
            old_meal_index = index
            break

    # replace old meal with our new choice
    days_meals[old_meal_index] = all_categories_meals[category][meal_number]

    # convert the days meals back into tuple
    plan[day_number - 1] = tuple(days_meals)

    return plan    

def confirm_plan(plan):
    # loop until break
    while True:
        print_plan(plan)
        
        print('[Day Number] to Replace Meal for that Day')
        print('[Enter] to Export Plan and Shopping List')
        
        choice = input()
        
        # check if integer input
        try:
            int_choice = int(choice)
            replace_meal(plan, int_choice)
        # not integer input
        except ValueError:
            if choice == '': # enter key
                export_plan(plan)
                export_shopping_list(plan)
                print('Meal Plan and Shopping List Both Exported')
                break
            else:
                print('Invalid Menu Option')

def print_welcome_header():
    print('\n========================')
    print('      Meal Planner      ')
    print('========================\n')
    
def print_plan(plan):
    print('\n----- Meal Plan -----\n')
    # print each day
    for day_number, day in enumerate(plan, start=1):
        print('Day', day_number)
        for meal in day:
            print('\t %s - %s' % (meal.category, meal.name))

    print('\n---------------------\n')
    
def create_plan_from_template(plan):
    templates_loader = FileSystemLoader(searchpath='./templates/')
    templates_environment = Environment(loader=templates_loader)
    template_plan = templates_environment.get_template('template_meal_plan.md')
    return template_plan.render(plan=plan)

def export_plan(plan):
    file_contents = create_plan_from_template(plan)
    formatted_datetime = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    filepath = 'exported_plan-' + formatted_datetime + '.md'
    # write file contents to file
    with open(filepath, 'w') as plan_file:
        plan_file.write(file_contents)

def create_shopping_list_from_template(plan):
    templates_loader = FileSystemLoader(searchpath='./templates/')
    templates_environment = Environment(loader=templates_loader)
    template_shopping_list = templates_environment.get_template('template_shopping_list.md')
    return template_shopping_list.render(plan=plan)

def export_shopping_list(plan):
    file_contents = create_shopping_list_from_template(plan)
    formatted_datetime = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    filepath = 'exported_shopping_list-' + formatted_datetime + '.md'
    # write file contents to file
    with open(filepath, 'w') as shopping_list_file:
        shopping_list_file.write(file_contents)

def generate_plan(number_of_days, categories):
    all_meals = get_meals_from_file()
    meals_by_category = []
    
    # iterate over each category
    for category in categories:
        meals_by_category.append(random.choices(all_meals[category], k=number_of_days))
    
    return list(zip(*meals_by_category)) # *-operator to unpack the arguments
    
if __name__ == '__main__':
    print_welcome_header()
    
    number_of_days, categories = get_plan_details()
    plan = generate_plan(number_of_days, categories)

    confirm_plan(plan)
