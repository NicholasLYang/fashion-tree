import urllib2

#response = urllib2.urlopen('https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=?'), (keyword,)
response = urllib2.urlopen('https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=jeans')

print(response.info())