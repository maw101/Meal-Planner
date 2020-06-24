from os import path
from dataclasses import dataclass

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