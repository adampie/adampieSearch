import requests
from envparse import env
from urllib import request, parse
from textblob import TextBlob, blob, Word
from bs4 import BeautifulSoup as soup
import MySQLdb
import random


def indexUrl():
    # Connect to MySQL DB
    env.read_envfile()
    db = MySQLdb.connect(env.str("db_ip"), env.str("db_user"), env.str("db_pass"), env.str("db_schema"))
    connect = db.cursor()

    # Set target url
    connect.execute("SELECT address FROM crawled_urls WHERE parsed=1 ORDER BY id ASC LIMIT 1;")
    results = connect.fetchone()
    target = results[0]
    updateUrl = "UPDATE crawled_urls SET parsed = 2 WHERE address = '" + target + "';"

    # Check for HTTP errors
    try:
        response = requests.get(target)
    except requests.exceptions.ConnectionError as e:
        connect.execute(updateUrl)

    # Get page
    site = None
    parsed = None
    try:
        site = request.urlopen(target).read()
        parsed = soup(site, 'html.parser')
    except:
        connect.execute(updateUrl)

    # Clean up HTML
    try:
        for tag in parsed.find_all(['script', 'style']):
            tag.replaceWith('')
        clean = parsed.get_text()
        blobText = TextBlob(clean)
    except:
        connect.execute(updateUrl)

    # Get NOUNS from text
    words = list()
    keyWords = ''
    try:
        for word, tag in blobText.tags:
            if tag == 'NN':
                words.append(word.lemmatize())
    except:
        connect.execute(updateUrl)
    try:
        for item in random.sample(words, 20):
            word = Word(item)
            if "'" not in word:
                keyWords = keyWords + ' ' + word.singularize()
        try:
            # Insert page into database
            insertSite = "INSERT INTO indexed_urls(address, title, keywords) VALUES ('" + target + "','" + parsed.title.string + "','" + keyWords + "');"
            connect.execute(insertSite)
            print("Done - " + target)
        except:
            print("Error in gathered data on page - " + target)
    except:
        print("Not enough data")
        connect.execute(updateUrl)

    # Set URL to indexed and close connections
    connect.execute(updateUrl)
    db.commit()
    connect.close()
    db.close()

    # Back at it again
    indexUrl()

indexUrl()

