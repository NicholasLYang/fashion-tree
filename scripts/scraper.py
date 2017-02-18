import urllib.request

url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=wranglers'

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open( url )
HTML = response.read().decode('utf-8')

ul_start = HTML.find('<ul id="s-results-list-atf"')
ul_end = HTML.find('<ul>', ul_start)
ul = HTML[ul_start : ul_end]

items = ul.split('<a class="a-link-normal a-text-normal"')

i = 10;

for item in items:
	if i == 0:
		break
	if not "jpg" in item:
		href_start = item.find('https://')
		href_end = item.find('">', href_start)
		href = item[href_start : href_end]
		i -= 1
		print(href)

