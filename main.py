#!/usr/bin/env python3
import argparse
from urllib.parse import urlparse

from allrecipes import AllRecipes as ar
from pyhellofresh.recipe import Recipe

def convert_url_to_name(url: str):
    if url.endswith("/"):
        url = url[:-1]
    return urlparse(url).path.split("/")[-1].replace("-"," ").title()

def allrecipes_recipe_to_markdown(recipe):
    """
    Converts a recipe dictionary to an Obsidian Markdown file.

    Args:
        recipe_dict (dict): A recipe dictionary with the following keys:
            cook_time (int): Estimated cooking time in minutes.
            ingredients (list): List of recipe ingredients as strings.
            name (str): The name of the recipe.
            nb_servings (int): Estimated number of servings.
            prep_time (int): Estimated preparation time in minutes.
            rating (float): Average rating of the recipe (0-5).
            steps (list): List of recipe steps as strings.
            total_time (int): The total cooking time of the recipe.
            url (str): The URL of the recipe. 

    Returns:
        str: A Markdown string representing the recipe.
    """

    markdown_lines = []

    # Add properties
    markdown_lines.append("---")
    markdown_lines.append("aliases:")
    markdown_lines.append(f"source: { recipe.get('url', '') }")
    markdown_lines.append("tags:")
    markdown_lines.append(f"rating: { '' if recipe.get('rating', None) == None else recipe['rating'] }")
    markdown_lines.append("---")
        
    markdown_lines.append(f"# {recipe.get('name')}\n")
    
    # Add info
    info_names = {
        "cook_time": "Cook Time",
        "prep_time": "Prep Time",
        "total_time": "Total Time",
        "nb_servings": "Servings"
    }
    for key in ["nb_servings", "prep_time", "cook_time", "total_time" ]:
        value = recipe.get(key)
        if value:
            markdown_lines.append(f"{info_names[key]}: {value}")

    markdown_lines.append("\n> Notes: \n")

    # Add ingredients as a checklist
    markdown_lines.append("## Ingredients")
    markdown_lines.append("#ingredients")
    markdown_lines.extend(f"- [ ] {ingredient['qty']}" for ingredient in recipe["ingredients"])
    markdown_lines.append("\n")

    # Add steps as a numbered list
    markdown_lines.append("## Directions")
    markdown_lines.extend(f"{idx + 1}. {step}" for idx, step in enumerate(recipe["steps"]))
    markdown_lines.append("\n")
    
    # Return completed Markdown string
    return "\n".join(markdown_lines)


def hellofresh_recipe_to_markdown(recipe):
    """
    Converts a pyhellofresh recipe dictionary to an Obsidian Markdown file.

    Args:
        recipe_dict (dict): A recipe dictionary with the following keys:
            cook_time (int): Estimated cooking time in minutes.
            ingredients (list): List of recipe ingredients as strings.
            name (str): The name of the recipe.
            nb_servings (int): Estimated number of servings.
            prep_time (int): Estimated preparation time in minutes.
            rating (float): Average rating of the recipe (0-5).
            steps (list): List of recipe steps as strings.
            total_time (int): The total cooking time of the recipe.
            url (str): The URL of the recipe. 

    Returns:
        str: A Markdown string representing the recipe.
    """

    markdown_lines = []

    # Add properties
    markdown_lines.append("---")
    markdown_lines.append("aliases:")
    markdown_lines.append(f"source: { recipe.get('url', '') }")
    markdown_lines.append(f"tags: {','.join([t.replace(' ','-').lower() for t in recipe.get('tags',[])])}")
    markdown_lines.append("rating:")
    # markdown_lines.append(f"rating: { '' if recipe.get('rating', None) == None else recipe['rating'] }")
    markdown_lines.append("---")
        
    markdown_lines.append(f"# {recipe.get('title')}\n")
    
    # Add info
    info_names = {
        "prep_time": "Prep Time",
        "total_time": "Total Time",
        "servings": "Servings"
    }
    for key in ["servings", "prep_time", "total_time" ]:
        value = recipe.get(key)
        if value:
            markdown_lines.append(f"{info_names[key]}: {value}")

    markdown_lines.append("\n> Notes: \n")

    # Add ingredients as a checklist
    markdown_lines.append("## Ingredients")
    markdown_lines.append("#ingredients")
    markdown_lines.extend(f"- [ ] {ingredient['qty']} {ingredient['ingredient']}" for ingredient in recipe["ingredients"])
    markdown_lines.append("\n")

    # Add directions by section
    markdown_lines.append("## Directions\n")
    
    for section in recipe["instructions"]:
        if section["title"]:
            markdown_lines.append(f"### {section['title']}")
        for step in section["steps"]:
            markdown_lines.append(f"- {step}")
        markdown_lines.append("\n")
    
    # Return completed Markdown string
    return "\n".join(markdown_lines)

def write_recipe_to_file(recipe, outfile=None):
    # md_lines = allrecipes_recipe_to_markdown(recipe)
    md_lines = hellofresh_recipe_to_markdown(recipe)
    filename = outfile if outfile else f"{recipe['title']}.md"
    with open(filename, 'w') as md_file:
        md_file.write(md_lines)

def get_recipe(url):
    recipe = ar.get(url)  # Get the details of the first returned recipe (most relevant in our case)
    # If the recipe name wasn't scraped, guess it from the URL
    if not recipe.get("title", None):
        recipe['title'] = convert_url_to_name(recipe['url'])
    return recipe

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts an AllRecipe recipe to Obsidian Markdown")
    parser.add_argument("url", type=str, help="The URL to process")
    parser.add_argument("--outfile", type=str, required=False, help="The name of the file to write to")
    args = parser.parse_args()
    
    # recipe = get_recipe(args.url)
    recipe = Recipe(args.url).asdict()
    write_recipe_to_file(recipe, args.outfile)
    
    