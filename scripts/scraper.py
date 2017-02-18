from bs4 import BeautifulSoup
from lxml import html
import csv,os,json,re
import requests
import urllib.request

def scrape(keyword):
    url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' + keyword
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    links = soup.find_all('a', {'class': 'a-link-normal s-access-detail-page s-overflow-ellipsis a-text-normal'})[2:-1]

    extracted = ""
    for link in links[:10]:
        if link.find('/gp/') == 0:
            continue
        try:
            asin = re.search(r'B\w{9}', link.get('href')).group(0)
        except:
            print(link.get('href'))
        print(asin)
        extracted += "\n" + (AmzonParser("http://amazon.com/dp/" + asin))

    f = open('data.json','w')
    json.dump(extracted,f,indent=4)

def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    while True:
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_MATERIAL = '//a[@class="a-link-normal a-color-tertiary"]//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_MATERIAL = doc.xpath(XPATH_MATERIAL)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            MATERIAL = ' > '.join([i.strip() for i in RAW_MATERIAL]) if RAW_MATERIAL else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            data = {
                    'NAME': NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'MATERIAL':MATERIAL,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'URL':url,
                    }

            return data
        except Exception as e:
            print(e)

def parse_item(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open( url )
    HTML = response.read().decode('utf-8')
    msg = ""

    name_start = HTML.find('<span id="productTitle" class="a-size') + 46
    name_end = HTML.find('</span>',name_start)
    msg += HTML[name_start:name_end].strip() + ","

    msg += url + ","

    price_start = HTML.find('<span id="priceblock_ourprice"')
    price_end =HTML.find('</span>',price_start)
    price = HTML[price_start:price_end]
    price = price[price.find('>')+1:]
    msg += price + ","

    rating = " "
    msg += rating + ","

    ul_start = HTML.find('<ul class="a-vertical a-spacing-none"')
    ul_end = HTML.find('</ul>',ul_start)
    ul = HTML[ul_start:ul_end]
    ul = ul.split('<li><span class="a-list-item">')[1:]
    for item in ul:
        if '%' in item:
            msg += item.replace('</span></li>','').strip() + ","

    return msg

scrape('jeans')
