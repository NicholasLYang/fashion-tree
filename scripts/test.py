import urllib2

url = 'https://www.amazon.com/Wrangler-Authentics-Classic-Regular-Stonewash/dp/B00XKXN95W/ref=sr_1_2?ie=UTF8&qid=1487393556&sr=8-2&keywords=wranglers'

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open( url )
html_contents = response.read()

