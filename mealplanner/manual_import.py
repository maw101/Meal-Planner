from sys import stdin
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


def manual_recipe_import():
    pass


def create_recipe_from_template(recipe_object):
    pass


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
