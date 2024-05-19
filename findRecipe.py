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

text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'li']

webUrl = input("Please enter a recipe website URL: ")
req = requests.Session()
html_text = req.get(webUrl, headers=headers).text
beaut = BeautifulSoup(html_text, 'lxml')

def findIngredients(soup):
    ingredient_class_list = []
    ingredient_class_list = findSpecificname('ingredients', ingredient_class_list)
    for single_ingredients in ingredient_class_list:
        texts = single_ingredients.find_all(text_tags)
        for text in texts:
            print(text.text)

def findSpecificname(name, list):
    for ingredients in beaut.find_all('div', class_=True):
        for c_name in ingredients["class"]:
            split_c_name = c_name.split('-')
            if "ingredients" in split_c_name:
                list.append(ingredients)
                return list


if __name__ == '__main__':
    findIngredients(beaut)
