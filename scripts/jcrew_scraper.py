from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import csv
import score_calculator
search_uri = "https://www.jcrew.com/r/search/?N=0&Nloc=en&Ntrm=%s&Npge=1&Nrpp=60&Nsrt=0"

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }
    result = requests.get(url, headers=headers)
    return BeautifulSoup(result.content, "html.parser")


def get_search_results(search_term):
    search_url = search_uri % search_term
    search_page = get_page(search_url)
    links = search_page.find_all('a', class_ = "product-tile__link")
    url_regex = r'(?<=href=").*(?=")'
    product_pages = []
    for link in links:
        m = re.search(url_regex, str(link))
        product_pages.append("https://jcrew.com" + m.group(0))
    return product_pages


def parse_product_page(product_url):
    product_page = get_page(product_url)
    output = {}
    output['link'] = product_url
    output['picture'] = scrape_image(product_page)
    output['name'] = scrape_product_name(product_page)
    output['price'] = scrape_product_price(product_page)
    output['section'] = scrape_section(output['name'])
    output['materials'] = scrape_materials(product_page)
    output['brand'] = 'Uniqlo'
    return output

def scrape_product_price(product_page):
    price_class = "product__variation--price-list product__price--list"
    return product_page.find('span', class_ = price_class).text

def scrape_product_name(product_page):
    return product_page.find('h1', class_ = "product__name").text

def scrape_image(product_page):
    image_div = product_page.find('img')
    print(image_div)
    image_url_regex = r'https://.*\"'
    image_url = re.search(image_url_regex, str(image_div))
    return image_url.group(0)

def scrape_section(product_url):
    sections = ['girl', 'boy', 'women', 'men']
    for section in sections:
        if section in product_url.lower():
            return section
    return None

def scrape_materials(product_page):
    specs = product_page.find('ul', class_ = 'prodspec').text
    materials_regex = r'[0-9]{1,3}% [^,|/|\n]*'
    materials = re.findall(materials_regex, specs)
    return materials

def parse_pages(keyword):
    product_pages = get_search_results(keyword)
    output = []
    for page in product_pages:
        product = parse_product_page(page)
        if product == None:
            continue
        product['keyword'] = keyword
        product['score'] = score_calculator.main(product['materials'])
        if product['score'] != None:
            output.append(product)
    return output


def write_to_csv(products, number):
    with open('jcrew' + str(number) + '.csv', 'w') as csvfile:
        field_names = products[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        for product in products:
            writer.writerow(product)


keywords = ['pants', 'shirts', 'tshirts', 'sweaters', 'coats', 'jackets']
def main():
    number = 0
    for keyword in keywords:
        products = parse_pages(keyword)
        write_to_csv(products, number)
        number = number + 1

main()
