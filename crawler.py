from envparse import env
from bs4 import BeautifulSoup
from urllib import parse, request
import MySQLdb

env.read_envfile()

target = "https://news.ycombinator.com/"

site = request.urlopen(target).read()
soup = BeautifulSoup(site, 'html.parser')

for tag in soup.findAll('a', href=True):
    print(parse.urljoin(target, tag['href']))
