from envparse import env
from prettytable import PrettyTable
import argparse
import MySQLdb


# Connect to MySQL DB
env.read_envfile()
db = MySQLdb.connect(env.str("db_ip"), env.str("db_user"), env.str("db_pass"), env.str("db_schema"))
connect = db.cursor()

# Set up args for command line
parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()

# Get results from database
query = "SELECT title, address FROM indexed_urls WHERE title LIKE '%"+args.input+"%' OR keywords LIKE '%"+args.input+"%' LIMIT 50;"
connect.execute(query)

# Create a sweet table with the results
results = PrettyTable(['Title', 'URL'])
results.align = "l"

# Add results to table and print
for site in connect.fetchall():
    results.add_row([site[0], site[1]])
print(results)
connect.close()
db.close()