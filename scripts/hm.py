from bs4 import BeautifulSoup
import urllib.request, requests
import re
import score_calculator

def main():
    queries = ['Sweaters & Cardigans', 'Shirts', 'Jeans', 'Jackets & Coats', 'Hoodies & Sweatshirts', 'Pants', 'T-shirts & Tank tops', 'Basics', 'Jackets & Suits', 'Accessories', 'Shoes', 'Underwear & Loungewear', 'Sportswear', 'Swimwear', 'Shorts', 'Casual', 'Divided', 'H&M Man', 'Modern Classics']
    output = "picture,price,score,link,material,name,keyword,section,brand"
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
    # picture
    image_start = HTML.find('lp.hm.com')
    image = HTML[image_start:HTML.find('"',image_start)]
    image = "https://" + image
    if "," in image:
        row += '"' + image + '",'
    else:
        row += image + ","
    # price
    price = re.search(r'\$\d{1,2}\.\d{2}',HTML[HTML.find('text-price'):]).group(0)
    row += price + ","
    # score
    material_start = HTML.find('text-information') + 18
    material = HTML[material_start:HTML.find('.',material_start)].replace('metallic fiber','metallic-fiber')
    materials = material.split(', ')
    try:
        score = score_calculator.main(materials)
    except:
        score = 10.98 # metal
    row += str(score) + ","
    # link
    row += url + ","
    # material
    row += material + ","
    # name
    name_end = HTML.find('<span class="price"')
    name = HTML[HTML.rfind('>',name_end-100,name_end)+1:name_end].strip()
    row += name + ","
    # keywords
    row += keyword + ","
    # section
    section_start = HTML.find('<a href="http://www.hm.com/us/department/') + 41
    section_end = HTML.find('</a>',section_start)
    section = HTML[section_start:section_end]
    section = section[:section.find('"')]
    row += section + ","
    # brand
    row += "hm,"
    print("processed " + name)
    return row

main()
