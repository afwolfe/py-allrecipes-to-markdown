# py-allrecipes-to-markdown

Uses [remaudcorentin-dev/python-allrecipes](https://github.com/remaudcorentin-dev/python-allrecipes) to parse recipes into Markdown for use in Obsidian or elsewhere.

The template is based on the one provided in this Obsidian Forum post: https://forum.obsidian.md/t/obsidian-as-recipe-manager-and-shopping-list-tutorial/40799

## Usage

```shell
python install -r requirements.txt # Install dependencies
python main.py $ALL_RECIPES_URL [--outfile path/to/file.md] # Convert the provided recipe to Markdown
```