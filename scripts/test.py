<<<<<<< HEAD
import urllib2
import re
=======
import urllib.request
>>>>>>> eb58ef21ae92a2111fad0b893020d3130ed60949

url='https://www.amazon.com/Nautica-Jeans-Relaxed-Rigger-34Wx30L/dp/B005BNJ5XY/ref=sr_1_13?s=apparel&ie=UTF8&qid=1487398326&sr=1-13&nodeID=7141123011&keywords=jeans&refinements=p_n_feature_eighteen_browse-bin%3A14630392011'
def main():
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open( url )
    HTML = response.read()

<<<<<<< HEAD
    ul_start = HTML.find('<ul class="a-vertical a-spacing-none"')
    ul_end = HTML.find('</ul>',ul_start)
    ul = HTML[ul_start:ul_end]
    ul = ul.split('<li><span class="a-list-item">')[1:]
=======
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open( url )
html_contents = response.read()
>>>>>>> eb58ef21ae92a2111fad0b893020d3130ed60949

    for item in ul: 
        if '%' in item:
            return item.replace('</span></li>','').strip()
main()
