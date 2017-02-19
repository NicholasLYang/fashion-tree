from bs4 import BeautifulSoup
import urllib.request
import requests
import re

def main():
    output = "picture,price,score,link,material,name,keyword,brand,gender"
    queries = ['Sweaters & Cardigans', 'Shirts', 'Jeans', 'Jackets & Coats', 'Hoodies & Sweatshirts', 'Pants', 'T-shirts & Tank tops', 'Basics', 'Jackets & Suits', 'Accessories', 'Shoes', 'Underwear & Loungewear', 'Sportswear', 'Swimwear', 'Shorts', 'Casual', 'Divided', 'H&M Man', 'Modern Classics']
    output = "picture,price,score,link,material,name,keyword,brand,gender"
    for q in queries:
        output += query(q)
    f = open('hm.csv','w',errors='ignore')
    f.write(output)
    f.close()


def query(q):    
    url = 'http://www.hm.com/us/products/search?q=' + q
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    links = soup.find_all('a', {'target': '_self'})
    output = ""
    for link in links:
        output += "\n" + parse_item(link.get('href'),q)
    print("-----COMPLETED " + q)
    return output
    
def parse_item(url,keyword):
    row = ""
    
    f = urllib.request.urlopen(url)
    HTML = f.read().decode('utf-8')
    
    image_start = HTML.find('lp.hm.com')
    image = HTML[image_start:HTML.find('"',image_start)]
    image = "https://" + image
    if "," in image:
        row += '"' + image + '",'
    else:
        row += image + ","
    price = re.search(r'\$\d{1,2}\.\d{2}',HTML[HTML.find('text-price'):]).group(0)
    row += price + ","

    material_start = HTML.find('text-information') + 18
    material = HTML[material_start:HTML.find('.',material_start)].replace(',',' ')

    row += str(computeScore(material)) + ","
    row += url + ","
 
    row += material + ","
    name_end = HTML.find('<span class="price"')
    name = HTML[HTML.rfind('>',name_end-100,name_end)+1:name_end].strip()
    row += name + ","
    row += keyword+"," #keywords
    row += "hm," #brand
    gender_start = HTML.find('<a href="http://www.hm.com/us/department/') + 41
    gender_end = HTML.find('</a>',gender_start)
    gender = HTML[gender_start:gender_end]
    gender = gender[:gender.find('"')]
    row += gender+","
    print("processed " + name)
    return row

def computeScore(material):
    energy_consumption = {
        'cotton': 49,
        'wool': 8,
        'polyester': 109,
        'viscose': 71,
        'spandex': 135,
        'rayon': 68,
        'acrylic': 2,
        'nylon': 68,
        'metallic fiber': 536,
        'lyocell': 36,
        }
    water_consumption = {
        'cotton': 12500,
        'wool': 125,
        'polyester': 0,
        'viscose': 640,
        'spandex': 26,
        'rayon': 190,
        'acrylic': 2,
        'nylon': 2,
        'metallic fiber': 12,
        'lyocell':12,        
        }    
    materials = material.split('  ')
    score = 0.0
    for m in materials:
        m = m.split('% ')
        try:
            score += int(m[0]) / 100 * (energy_consumption[m[1]] + water_consumption[m[1]]) / 2
        except:
            score += 6.12
    return score

main()
