'''
import urllib.request
import re

link = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=wranglers'

def main():

	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open( link )
	HTML = response.read().decode('utf-8')

	ul_start = HTML.find('<ul id="s-results-list-atf"')
	ul_end = HTML.find('<ul>', ul_start)
	ul = HTML[ul_start : ul_end]

	items = ul.split('<a class="a-link-normal a-text-normal" href="')[1:]

	#print(items[0])
	i = 5;
	for item in items:
		if i == 0:
			break
		if not "jpg" in item:
			href_start = item.find('https://')
			href_end = item.find('"', href_start)
			href = item[href_start : href_end]
			img_start = item.find('images')
			img_end = item.find('.jpg')
			img = item[img_start : img_end]
			#i -= 1
		print(href)
def parse(url):
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open( url )
    HTML = response.read().decode('utf-8')

    ul_start = HTML.find('<ul class="a-vertical a-spacing-none"')
    ul_end = HTML.find('</ul>',ul_start)
    ul = HTML[ul_start:ul_end]
    ul = ul.split('<li><span class="a-list-item">')[1:]

    for item in ul: 
        if '%' in item:
            return item.replace('</span></li>','').strip()

main()
'''

from bs4 import BeautifulSoup
import requests
import urllib.request
# add header
def main(url):
	headers = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
	}
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.content, "html.parser")

	links = soup.find_all('a', {'class': 'a-link-normal s-access-detail-page a-text-normal'}) [2: ]
	img = soup.find_all('img', {'class': 's-access-image cfMarker'}) [2: ]

	D = []
	for link in links:
	    print("Link: " + link.get('href'))
	    D.append(parse_item(link.get('href')))
	return D

def parse_item(url):
    print("parsing "+url)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open( url )
    HTML = response.read().decode('utf-8')
    M = {}
    print(HTML)
    ul_start = HTML.find('<ul class="a-vertical a-spacing-none"')
    ul_end = HTML.find('</ul>',ul_start)
    ul = HTML[ul_start:ul_end]
    ul = ul.split('<li><span class="a-list-item">')[1:]
    for item in ul: 
        if '%' in item:
            M["MATERIAL"] = item.replace('</span></li>','').strip()

    title_start = HTML.find('<span id="productTitle" class="a-size')
    title_end = HTML.find('</span>',title_start)
    title = HTML[title_start:title_end].strip()
    M["NAME"] = title

    price_start = HTML.find('<span id="priceblock_ourprice"')
    price_end =HTML.find('</span>',price_start)
    price = HTML[price_start:price_end]
    price = price[price.find('>')+1:]
    M["PRICE"] = price

    return M

print(parse_item("https://www.amazon.com/VTech-CS6649-Expandable-Cordless-Answering/dp/B00839N5O8/ref=sr_1_16/163-3048179-2106338?ie=UTF8&qid=1487418005&sr=8-16&keywords=phone"))

"""
d=main("https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=phone&rh=i%3Aaps%2Ck%3Aphone")
f = open('hi.txt','w')
f.write(str(d))
f.close()
"""