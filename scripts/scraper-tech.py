from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import score_calculator

def header(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def find_wattage(battery, life):
	p = re.compile(r"[0-9]*(?= WH)")
	q = re.compile(r"[0-9]*(?=[ -]watt)")
	a = re.compile(r"[0-9]*(?= Hour)")
	if p.search(battery) and a.search(life):
		watt = int(int(re.findall(p,battery)[0])/int(re.findall(a,life)[0]))
		return watt
	elif q.search(battery):
		return re.findall(q,battery)[0]
	else:
		return 0


def parse_item(url):
    soup = header(url)
    row = ""
    f = open('hi.html','w')
    f.write(soup.prettify())
    f.close()
    # image
    span = soup.find('span', {'class' : 'mainSlide'})
    if span :
        src = span.findChildren()[0].get('src')
        row += src[2:] + ","
    else:
        row += ","

    # price
    row += ","
	
    # link
    row += url + ","
    
    # wattage and score
    w = soup.find_all('h3', {'class' : 'specTitle'})
    wat = 0
    for watt in w:
    	if watt.text == 'Power':
    		battery = watt.find_next_sibling().find_next_sibling()
    		battery_life = battery.find_next_sibling()
    		wat = find_wattage(str(battery),str(battery_life))	
    		if wat == 0:
    			row += ",,"
    			return row
    		else: 
    			score = str((int(wat) * -1.25) + 100)
    			row += score + "," + str(wat) + ","
  	
    # name and brand
    h1 = soup.find('h1', {'id' : 'grpDescrip_h'})
    if h1:
    	name = h1.findChildren()[0].text
    	row += name.strip().replace(",",'').replace('"','') + ","
    	brand = name.split(" ")[0]
    	row += brand + ","
    	print("processing" + name.strip())
    else:
    	row += ",,,"

    return row

def query(key):    
	url = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=" + key.replace(" ","+") + "&N=-1&isNodeId=1"
	soup = header(url)
	links = soup.find_all('a', {'class': 'item-title'})
	output = ""
	for link in links:
		output += "\n" + parse_item(link.get('href'))
		output += key
		print("-----COMPLETED " + key)
	return output

def main():
    queries = ['Lenovo Laptop', 'Asus Laptop', 'Apple Laptop', 'Toshiba Laptop', 'Dell Laptop', 'Razor Laptop', 'Samsung Laptop', 'HP Laptop']
    output = "picture,price,link,watts,score,name,brand,keyword"
    for key in queries[1:2]:
        output += query(key)
    f = open('newegg0.csv','w',errors='ignore')
    f.write(output)
    f.close()

main()
