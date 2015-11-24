import urllib2
from bs4 import BeautifulSoup
from retry import *
import codecs

@retry(urllib2.URLError, tries=100, delay=1, backoff=1)
def urlopen_with_retry(url):
    return urllib2.urlopen(url).read()

id = 1
with open("urls.txt") as f:
	for url in f:
		html = urlopen_with_retry(url)

		soup = BeautifulSoup(html, "html.parser")
		text = soup.get_text()
		with codecs.open("documentos_procesados1/" + str(id) + ".txt", "w", "utf-8-sig") as temp:
			temp.write(text)
		id += 1
