from bs4 import BeautifulSoup
import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # noqa
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    # noqa
}
# These are the tags the scapper looks at to find text data
text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'li']

# This helps to make more websites accessible to be scrapped
search_tags = ['div', 'section', 'article']

webUrl = input("Please enter a recipe website URL: ")
req = requests.Session()
html_text = req.get(webUrl, headers=headers).text
beaut = BeautifulSoup(html_text, 'lxml')

def findIngredients(soup):
    ingredient_class_list = []
    # Holds all the ingredient info to check for duplicates
    ingredient_text_list = []
    search_for_names = ['ingredients']
    ingredient_class_list = findSpecificname(search_for_names, ingredient_class_list)
    if ingredient_class_list[0] == 'empty':
        print("No ingredients found")
        return
    for single_ingredients in ingredient_class_list:
        texts = single_ingredients.find_all(text_tags)
        for text in texts:
            if text.text.split() not in ingredient_text_list:
                ingredient_text_list.append(text.text.split())
                print(text.text.strip())

def findInstructions(soup):
    instructions_class_list = []
    search_for_names = ['instructions', 'directions', 'steps']
    instructions_class_list = findSpecificname(search_for_names, instructions_class_list)
    instruction_text_tag = ['li']
    if instructions_class_list[0] == 'empty':
        print("No instructions found")
        return
    for single_instruction in instructions_class_list:
        texts = single_instruction.find_all(instruction_text_tag)
        for index, text in enumerate(texts):
            if text.text.strip() == "Ingredients" or text.text.strip() == "Directions":
                print(text.text.strip())
            else:
                print(f"{index}: {text.text.strip()}")

def findNotes(soup):
    notes_class_list = []
    search_for_names = ['notes']
    span_and_text = text_tags
    span_and_text.append('span')
    notes_class_list = findSpecificname(search_for_names, notes_class_list)
    if notes_class_list[0] == 'empty':
        print("No notes found")
        return
    for single_note in notes_class_list:
        texts = single_note.find_all(span_and_text)
        for text in texts:
            print(text.text)

def findSpecificname(names, list):
    for tag in search_tags:
        for recipe_item in beaut.find_all(tag, class_=True):
            for c_name in recipe_item["class"]:
                split_c_name = c_name.split('-')
                for name in names:
                    if name in split_c_name:
                        list.append(recipe_item)
                        return list
                split_c_name = c_name.split(' ')
                for name in names:
                    if name in split_c_name:
                        list.append(recipe_item)
                        return list
                split_c_name = c_name.split('__')
                for name in names:
                    if name in split_c_name:
                        list.append(recipe_item)
                        return list

    return ['empty']



if __name__ == '__main__':
    findIngredients(beaut)
    findInstructions(beaut)
    findNotes(beaut)
