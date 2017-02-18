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
        output += "\n" + parse_item(link.get('href'));

    return output + keyword
    
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
    score = 98
    row += str(score) + ","
    row += url + ","
    material_start = HTML.find('text-information') + 18
    material = HTML[material_start:HTML.find('.',material_start)].replace(','+' ')
    name_end = HTML.find('<span class="price"')
    name = HTML[HTML.rfind('>',name_end-100,name_end)+1:name_end].strip()
    row += name + ","

    return row

if name == '__main__':
    f = open('ex.csv','w')
    f.write(query('jeans'))
    f.close()
