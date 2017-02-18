import urllib2
import re

url='https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=pants&rh=i%3Aaps%2Ck%3Apants'
def parse(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open( url )
    HTML = response.read()

    ul_start = HTML.find('<ul id="s-results-list-atf"')
    ul_end = HTML.find('</ul>',ul_start)
    ul = HTML[ul_start:ul_end]
    ul = ul.split('<li id="result_')[1:]

    D = []
    for item in ul:
        link_start = item.find('<a class="a-size-small a-link-normal a-text-normal" href="') + 58 
        link_end = item.find('">',link_start)
        link = item[link_start:link_end]
        D.append(parse_item(link))
    return D

def parse_item(url):
    print("parsing "+url)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open( url )
    HTML = response.read()
    M = {}

    ul_start = HTML.find('<ul class="a-vertical a-spacing-none"')
    ul_end = HTML.find('</ul>',ul_start)
    ul = HTML[ul_start:ul_end]
    ul = ul.split('<li><span class="a-list-item">')[1:]
    for item in ul: 
        if '%' in item:
            M["MATERIAL"] = item.replace('</span></li>','').strip()

    title_start = HTML.find('<span id="productTitle" class="a-size')
    title_end = HTML.find('</span>',title_start)
    title = HTML[title_start:title_end][45:].strip()
    M["NAME"] = title

    price_start = HTML.find('<span id="priceblock_ourprice"')
    price_end =HTML.find('</span>',price_start)
    price = HTML[price_start:price_end]
    price = price[price.find('>')+1:]
    M["PRICE"] = price

    return M

