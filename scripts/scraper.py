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
url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=phone&rh=i%3Aaps%2Ck%3Aphone"
# add header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")

file = open("parseddata.txt", "w")

links = soup.find_all('a', {'class': 'a-link-normal s-access-detail-page a-text-normal'}) [2: ]
img = soup.find_all('img', {'class': 's-access-image cfMarker'}) [2: ]

for link in links:
    print("Link: " + link.get('href'))
    file.write(link.get('href')+ '\n')
file.close()
	
	

