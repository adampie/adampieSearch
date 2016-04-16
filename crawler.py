from envparse import env
from bs4 import BeautifulSoup
import urllib.request

env.read_envfile()

target = "https://news.ycombinator.com/"

site = urllib.request.urlopen(target).read()
soup = BeautifulSoup(site, 'html.parser')

for tag in soup.findAll('a', href=True):
    print(urllib.request.urljoin(target, tag['href']))
