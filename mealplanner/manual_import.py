from sys import stdin
from os import path, makedirs
import errno
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader

@dataclass
class Recipe:
    name: str = ''
    category: str = ''
    total_time: int = 0
    prep_time: int = 0
    cooking_time: int = 0
    rating: int = 0
    source: str = ''
    servings: int = 0
    calories: float = 0.0
    ingredients: str = ''
    instructions: str = ''


def manual_recipe_import():
    recipe = Recipe()
    
    # get name
    recipe.name = input('Enter recipe name: ')
    
    # get category
    recipe.category = input('Enter recipe category: ')
    
    # get prep time
    while True:
        try:
            input_val = int(input('Enter recipe prep time (integer): '))
            recipe.prep_time = input_val
            break
        except ValueError:
            print('Invalid Input, must be an integer value.')
            
    # get cooking time
    while True:
        try:
            input_val = int(input('Enter recipe cooking time (integer): '))
            recipe.cooking_time = input_val
            break
        except ValueError:
            print('Invalid Input, must be an integer value.')

    # calculate total time (prep time + cooking time)
    recipe.total_time = recipe.prep_time + recipe.cooking_time

    # get rating
    while True:
        try:
            input_val = float(input('Enter recipe rating (decimal/float): '))
            recipe.rating = input_val
            break
        except ValueError:
            print('Invalid Input, must be a decimal/float value (eg 9.0 or 9.5).')
        
    # get source
    recipe.source = input('Enter recipe source: ')
    
    # get servings
    while True:
        try:
            input_val = int(input('Enter recipe servings (integer): '))
            recipe.servings = input_val
            break
        except ValueError:
            print('Invalid Input, must be an integer value.')

    # get calories
    while True:
        try:
            input_val = float(input('Enter recipe calories (decimal/float): '))
            recipe.calories = input_val
            break
        except ValueError:
            print('Invalid Input, must be a decimal/float value (eg 100.0 or 100.5).')
    
    # get ingredients
    print('Enter recipe ingredients: ')
    recipe.ingredients = __get_multiline_as_string()
    
    # get instructions
    print('Enter recipe instructions: ')
    recipe.instructions = __get_multiline_as_string()
    
    # perform processing for recipe storage
    file_contents = create_recipe_from_template(recipe)
    filepath = get_recipe_filepath(recipe.name, recipe.category)

    # ensure directories exist
    if not path.exists(path.dirname(filepath)):
        try:
            makedirs(path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    
    # write file contents to file
    
    
    # read file contents from file
    


def create_recipe_from_template(recipe_object):
    templates_loader = FileSystemLoader(searchpath='./templates/')
    templates_environment = Environment(loader=templates_loader)
    template_recipe = templates_environment.get_template('template_recipe.md')
    return template_recipe.render(recipe=recipe_object)


def get_recipe_filepath(recipe_name, recipe_category):
    filename = recipe_name.lower().replace(' ', '_') + '.md'
    filepath = f'recipes/{recipe_category}/{filename}'
    # determine if file exists
    if path.isfile(filepath):
        overwrite_file = input('There already exists a recipe with these details, overwrite? \'Y\' or \'N\'')
        # check if going to overwrite
        if overwrite_file.upper() == 'Y':
            # start counter
            attempt = 1
            # loop while we have a duplicate filename
            while path.isfile(filepath):
                filename = recipe_name.lower().replace(' ', '_') + f'_{attempt}.md'
                filepath = f'recipes/{recipe_category}/{filename}'
                attempt += 1 # increment attempt number for case of loop
    return filepath


def __get_multiline_as_string():
    print('Once you have finished, press enter for a new line then press Ctrl+d for Unix systems, Ctrl+z for Windows systems.\n\n')
    lines = stdin.readlines()
    print('\n')
    return ' \n'.join(lines)


if __name__ == '__main__':
    manual_recipe_import()
