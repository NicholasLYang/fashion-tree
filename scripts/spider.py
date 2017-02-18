from bs4 import BeautifulSoup
import urllib.request
import requests
import re

url = "http://www.hm.com/us/product/20775?article=20775-D"

def query(keyword):
    url = "http://www.hm.com/us/products/search?q=" + keyword
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    output = "picture,price,score,link,material,name,keyword"

    links = soup.find_all('a', {'target': '_self'})
    for link in links:
        output += "\n" + parse_item(link.get('href')) + keyword

    return output
    
def parse_item(url):
    row = ""
    
    f = urllib.request.urlopen(url)
    HTML = f.read().decode('utf-8')
    
    image_start = HTML.find('lp.hm.com')
    image = HTML[image_start:HTML.find('"',image_start)]
    if "," in image:
        row += '"' + image + '",'
    else:
        row += image + ","
    price = re.search(r'\$\d{1,2}\.\d{2}',HTML[HTML.find('text-price'):]).group(0)
    row += price + ","

    material_start = HTML.find('text-information') + 18
    material = HTML[material_start:HTML.find('.',material_start)]

    row += str(computeScore(material)) + ","
    row += url + ","
 
    row += material + ","
    name_end = HTML.find('<span class="price"')
    name = HTML[HTML.rfind('>',name_end-100,name_end)+1:name_end].strip()
    row += name + ","

    return row

def computeScore(material):
    energy_consumption = {
        'cotton': 49,
        'wool': 8,
        'polyester': 109,
        'viscose': 71,
        'spandex': 135,
        'rayon': 68
        }
    water_consumption = {
        'cotton': 12500,
        'wool': 125,
        'polyester': 0,
        'viscose': 640,
        'spandex': 26,
        'rayon': 190
        }    
    materials = material.split(', ')
    score = 0.0
    for m in materials:
        m = m.split('% ')
        score += int(m[0]) / 100 * (energy_consumption[m[1]] + water_consumption[m[1]]) / 2
    return score

f = open('ex.csv','w',errors='ignore')
f.write(query('jeans'))
f.close()
