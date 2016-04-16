from envparse import env
from bs4 import BeautifulSoup as soup
from urllib import parse, request, robotparser
import MySQLdb

# Connect to db
env.read_envfile()
db = MySQLdb.connect(env.str("db_ip"), env.str("db_user"), env.str("db_pass"), env.str("db_schema"))
connect = db.cursor()

# Set target URL and root domain
connect.execute("SELECT address FROM crawled_urls WHERE parsed=0 ORDER BY id ASC LIMIT 1;")
results = connect.fetchone()
target = results[0]
root_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=request.urlparse(target))

# Check robots.txt
robots = robotparser.RobotFileParser()
robots_url = parse.urljoin(root_domain, "robots.txt")
robots.set_url(robots_url)
robots.read()

site = request.urlopen(target).read()
soup = soup(site, 'html.parser')

for tag in soup.findAll('a', href=True):
    if robots.can_fetch('*', parse.urljoin(target, tag['href'])):
        print("ALLOWED - " + parse.urljoin(target, tag['href']))
    else:
        print("DISALLOWED - " + parse.urljoin(target, tag['href']))


