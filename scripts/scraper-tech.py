from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import csv

def header(url):
	headers = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
	}
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.content, "html.parser")
	return soup

def gen_url(key):
	url = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=" + key.replace(" ","+") + "&N=-1&isNodeId=1"
	return url

def main(key):
	soup = header(gen_url(key))
	links = soup.find_all('a', {'class': 'item-img'})
	img = []
	for link in links:
		children = link.findChildren()
		img.append(children[0])
	O = "Name,Link,Rating,Wattage,Image,Keyword"
	i = 0;
	while i < len(links):
		O += "\n" + parse_item(links[i].get('href'))
		O += img[i].get('src').replace("//","") + ","
		O += key + "/n"
		i += 1
	return O

def find_Wattage(battery, life):
	p = re.compile(r"[0-9]*(?= WH)")
	q = re.compile(r"[0-9]*(?= mAh)")
	r = re.compile(r"[0-9]*(?=[ -]watt)")
	a = re.compile(r"[0-9]*(?= Hour)")
	if p.search(battery) and a.search(life):
		watt = round(int(re.findall(p,battery)[0])/int(re.findall(a,life)[0]))
		return watt
	elif q.search(battery) and a.search(life):
		watt = round(int(re.findall(q,battery)[0])/int(re.findall(a,life)[0]))
		return watt
	elif r.search(battery):
		return re.findall(r,battery)[0]
	else:
		return "Cannot compute wattage!"


def parse_item(url):
	soup = header(url)
	print(url)
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open( url )
	HTML = response.read().decode('utf-8')
	msg = ""

	#name of product
	h1 = soup.find('h1', {'id' : 'grpDescrip_h'})
	name = h1.findChildren()[0].text

	msg += name.strip().replace(",","") + "," + url + ","

	#getting wattage
	w = soup.find_all('h3', {'class' : 'specTitle'})
	wat = 0
	for watt in w:
		if watt.text == 'Power':
			battery = watt.find_next_sibling().find_next_sibling()
			battery_life = battery.find_next_sibling()
			wat = find_Wattage(str(battery),str(battery_life))	
	if wat == 0:
		msg += "," + ","
		return msg
	else: 
		msg += "," + str(wat) + ","
	return msg

#parse_item('https://www.newegg.com/Product/Product.aspx?Item=9SIA60G3ZE0281&cm_re=google_laptops-_-9SIA60G3ZE0281-_-Product')

d=main('google laptops')
f=open('newegg.csv','a')
f.write(d)
f.close()
'''
input_file = 'newegg.csv'
output_file = 'NEWegg.csv'

with open(input_file) as f1:
    lines = f1.readlines()

for line in lines:
    watt = line.split(",")[3]
    if watt.isnumeric():
    	with open(output_file, 'w') as myfile:
            myfile.write(line)

f1.close()
myfile.close()
'''