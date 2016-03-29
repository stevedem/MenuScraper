# This script will:
# Go to an AllMenus URL provided as the site variable, produce a list of all URLs found on that page
# and write out text files containing 50 links.

# Author: Steven DeMarco

import urllib2
from random import randint
import time
from BeautifulSoup import BeautifulSoup

links = []
sites = list()
sites.append('http://www.allmenus.com/pa/pittsburgh/-/?sort=popular&filters=none')
sites.append('http://www.allmenus.com/pa/philadelphia/-/?sort=popular&filters=none')
sites.append('http://www.allmenus.com/ny/new-york/-/?sort=popular&filters=none')
sites.append('http://www.allmenus.com/md/baltimore/-/?sort=popular&filters=none')

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

for site in sites:
    time.sleep(randint(0, 60))
    # Generate the HTTP request
    req = urllib2.Request(site, headers=hdr)

    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()

    # Read the page content
    content = page.read()

    # Generate a result set from the HTML tags
    soup = BeautifulSoup(content)

    # Find all div tags with and id = restaurant_list
    for restaurant_list in soup.findAll("div", {"id": "restaurant_list"}):
        # Find all div tags with the class = basics
        for basics in restaurant_list.findAll("div", {"class": "basics"}):
            # Find all a tags that have an href
            for a in basics.findAll('a', href=True):
                # Concat all hyperlinks to the base URL and add to list
                links.append("http://www.allmenus.com/" + a['href'])

# Write out the links to a text file
with open('links/links.txt', 'wb') as links_file:
        for link in links:
            links_file.write("%s\n" % link)

# Inform the user how many links were collected
print "Grabbed " + str(len(links)) + " links."
