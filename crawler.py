from envparse import env
from bs4 import BeautifulSoup
import urllib
import urlparse
import MySQLdb

env.read_envfile()

target = "https://news.ycombinator.com/"

site = urllib.urlopen(target).read()
soup = BeautifulSoup(site, 'html.parser')

for tag in soup.findAll('a', href=True):
    print(urlparse.urljoin(target, tag['href']))
