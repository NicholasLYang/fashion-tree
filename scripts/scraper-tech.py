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

def main():
    output = "picture,price,link,wattage,score,name,category,brand,keyword"
    queries = ['Lenovo Laptop', 'Asus Laptop', 'Apple Laptop', 'Toshiba Laptop', 'Dell Laptop', 'Razor Laptop', 'Samsung Laptop', 'HP Laptop']
    output = "picture,price,link,wattage,score,name,category,brand,keyword"
    for key in queries:
        output += query(key)
    f = open('newegg.csv','w',errors='ignore')
    f.write(output)
    f.close()

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

def parse_item(url):
    soup = header(url)
    row = ""

    # image
    span = soup.find('span', {'class' : 'mainSlide'})
    if span :
        src = span.findChildren()[0].get('src')
        row += src + ","
    else:
        row += ","

    # price
    if soup.find('div', {'class' : 'price-current'}):
        p = soup.find('div', {'class' : 'price-current'}).text
    else:
        p = soup.find('div', {'class' : 'price-display-item regular-price'}).text
    q = re.compile("\d+\.\d+")
    price = q.findall(p)[0]
    row += price + ","

    # link
    row += url + ","

    # material and score
    div2 = soup.find('div', {'class' : 'product-details-and-care'})
    r = re.compile("\d+\%")
    ul = div2.findChildren()[0].find_next_sibling()
    m = ul.find('li', {'data-reactid' : r})
    if m:
        material = m.text
        row += material.replace(',',' ') + "," + str(computeScore(material)) + ","
    else:
        row += ",,"

    # name
    section = soup.find('section', {'class' : 'np-product-title'})
    name = section.findChildren()[0].text
    row += name + ","

    # category
    li = soup.find('li', {'data-element' : 'item_1'})
    category = li.findChildren()[0].text
    row += category + ","

    # brand
    section = soup.find('section', {'class' : 'brand-title'})
    data = section.findChildren()
    row += "Nordstorm,"
    print("processing" + name)
    return row

parse_item('https://www.newegg.com/Product/Product.aspx?Item=N82E16834332305&cm_re=lenovo_laptop-_-34-332-305-_-Product')

'''
def main(key):
	soup = header(gen_url(key))
	links = soup.find_all('a', {'class': 'item-title'})
	img = []
	for link in links:
		children = link.findChildren()
		img.append(children[0])
	O = "name,link,rating,wattage,picture,keyword"
	O = ""
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
		watt = int(int(re.findall(p,battery)[0])/int(re.findall(a,life)[0]))
		return watt
	elif q.search(battery) and a.search(life):
		watt = int(int(re.findall(q,battery)[0])/int(re.findall(a,life)[0]))
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

	msg += name.strip().replace(",","").replace('"',"") + "," + url + ","

	#getting wattage
	w = soup.find_all('h3', {'class' : 'specTitle'})
	wat = 0
	for watt in w:
		if watt.text == 'Power':
			battery = watt.find_next_sibling().find_next_sibling()
			battery_life = battery.find_next_sibling()
			wat = find_Wattage(str(battery),str(battery_life))	
	if wat == 0 or wat == "Cannot compute wattage!":
		msg += ",,,"
		return msg
	else: 
		score = str((int(wat) * -1.25) + 100)
		msg += score + str(wat) + ","
	return msg

#parse_item('https://www.newegg.com/Product/Product.aspx?Item=9SIA60G3ZE0281&cm_re=google_laptops-_-9SIA60G3ZE0281-_-Product')

#google laptops
d=main('msi laptops')
f=open('newegg-msi.csv','a')
f.write(d)
f.close()
'''
