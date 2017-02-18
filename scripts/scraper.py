from bs4 import BeautifulSoup
import requests
import urllib.request

def main(url):
	headers = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
	}
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.content, "html.parser")

	links = soup.find_all('a', {'class': 'a-link-normal s-access-detail-page a-text-normal'}) [2: ]
	img = soup.find_all('img', {'class': 's-access-image cfMarker'}) [2: ]
	O = "Name,Material,Price,Image"
	
	i = 0;
	while i < len(links):
		O += "\n" + parse_item(links[i].get('href'))
		O += img[i].get('src')
		i += 1

	return O

def parse_item(url):
	print(url)
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open( url )
	HTML = response.read().decode('utf-8')
	msg = ""

	name_start = HTML.find('<span id="productTitle" class="a-size') + 46
	name_end = HTML.find('</span>',name_start)
	msg += HTML[name_start:name_end].strip() + ","

	ul_start = HTML.find('<ul class="a-vertical a-spacing-none"')
	ul_end = HTML.find('</ul>',ul_start)
	ul = HTML[ul_start:ul_end]
	ul = ul.split('<li><span class="a-list-item">')[1:]
	for item in ul: 
	    if '%' in item:
	        msg += item.replace('</span></li>','').strip() + ","

	price_start = HTML.find('<span id="priceblock_ourprice"')
	price_end =HTML.find('</span>',price_start)
	price = HTML[price_start:price_end]
	price = price[price.find('>')+1:]
	msg += price + ","

	return msg