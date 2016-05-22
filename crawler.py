from envparse import env
from bs4 import BeautifulSoup as soup
from urllib import parse, request, robotparser
import MySQLdb

def crawlUrl():

    # Connect to MySQL DB
    env.read_envfile()
    db = MySQLdb.connect(env.str("db_ip"), env.str("db_user"), env.str("db_pass"), env.str("db_schema"))
    connect = db.cursor()

    # Set target URL and root domain
    connect.execute("SELECT address FROM crawled_urls WHERE parsed=0 ORDER BY id ASC LIMIT 1;")
    results = connect.fetchone()
    target = results[0]
    root_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=request.urlparse(target))

    # Check robots.txt
    try:
        robots = robotparser.RobotFileParser()
        robots_url = parse.urljoin(root_domain, "robots.txt")
        robots.set_url(robots_url)
        robots.read()
    except:
        print("Check robots.txt error")

    # I do like a good Soup
    updateUrl = "UPDATE crawled_urls SET parsed = 1 WHERE address = '" + target + "';"
    try:
        site = request.urlopen(target).read()
        parsed = soup(site, 'html.parser')

        # Go through the URLS
        for tag in parsed.findAll('a', href=True):
            url = parse.urljoin(target, tag['href'])
            existsAndCrawled = "SELECT (parsed = 1) AS a_equals_b FROM crawled_urls WHERE address = '" + url + "';"
            insertUrl = "INSERT INTO crawled_urls(address) VALUES ('" + url + "');"

            # If can fetch and site is new then insert to db
            if robots.can_fetch('*', url):
                if connect.execute(existsAndCrawled) == 0:
                    connect.execute(insertUrl)
                    print("Added - "+url)
    except:
        print("Soup/Parsing error")
        connect.execute(updateUrl)

    # Set URL to parsed and close connections
    connect.execute(updateUrl)
    db.commit()
    connect.close()

    # Back at it again
    crawlUrl()

crawlUrl()
