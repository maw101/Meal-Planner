from dataclasses import dataclass, field
from typing import List
import re

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

