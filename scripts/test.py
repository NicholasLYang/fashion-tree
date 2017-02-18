import urllib.request
import re


def parse(url):
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open( url )
    HTML = response.read()

    ul_start = HTML.find('<ul class="a-vertical a-spacing-none"')
    ul_end = HTML.find('</ul>',ul_start)
    ul = HTML[ul_start:ul_end]
    ul = ul.split('<li><span class="a-list-item">')[1:]

    for item in ul: 
        if '%' in item:
            return item.replace('</span></li>','').strip()
main()
