# This script will:
# Utilize the links provided as a result of grab_links.py and scrape the web page to
# generate text files for each restaurant's menu.

# Note: This script will prompt the user to determine which links file they wish to use.
#   - This is to avoid being blocked by the AllMenus website.
#   - 50 links per scrape is a reasonable amount of traffic for any singular IP address.

# Author: Steven DeMarco

import sys
import urllib2
import csv
import time
from BeautifulSoup import BeautifulSoup
from random import randint

links = []
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


def clean(s):
    """ Cleans string.
    :param s: String
    :return: String
    """
    s = s.replace("&amp;", "&")
    s = s.replace(".", "")
    s = s.replace(",", "")
    s = s.replace("*", "")
    s = s.replace("&", "")
    s = s.replace("-", "")
    s = s.replace("(", "")
    s = s.replace(")", "")
    s = s.replace("$", "")

    return s

# Prompt user for the input file name
with open("links/links.txt", "rb") as links_file:
    links = [x.strip('\n') for x in links_file.readlines()]

# For each of the links in the specified file:
# Scrape the restaurant's name & geo-tag
# Scrape the menu item names and menu item descriptions from their online menus
# Write this to an individual text file corresponding to each restaurant's menu
for link in links:
    time.sleep(randint(0, 60))

    req = urllib2.Request(link, headers=hdr)

    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print "Failed on this link: " + link
        sys.exit(1)

    content = page.read()

    soup = BeautifulSoup(content)

    company_name = ''

    # Get the company's name and geo-tag
    for company in soup.findAll("div", {"id": "restaurant"}):
        for name in company.findAll("h1", {"itemprop": "name"}):
            company_name = name.text
        for latitude in company.findAll("meta", {"itemprop": "latitude"}):
            company_name += '_' + latitude["content"] + ","
        for longitutde in company.findAll("meta", {"itemprop": "longitude"}):
            company_name += longitutde["content"]

    # Notify the user which menu is currently being written
    print "Writing menu for: " + company_name
    print company_name + " URL: " + link

    # Save any alternative menus for processing
    alt_menu_links = list()
    for alt_menu in soup.findAll("div", {"id": "alternative_menus"}):
        for alt_link in alt_menu.findAll('a', href=True):
            full_URL = "http://www.allmenus.com" + str(alt_link['href'])
            if full_URL != link:
                alt_menu_links.append(full_URL)

    # Get all of the menu items and their corresponding descriptions
    menu_items = []

    for menu in soup.findAll("div", {"id": "menu"}):
        for category_div in menu.findAll("div", {"class": "category"}):
            for category_head in category_div.findAll("div", {"class": "category_head"}):
                for header in category_head.findAll("h3"):
                    h = clean(header.text)
                    if "beverage" in h.lower() or "beverages" in h.lower() or "drink" in h.lower() or "drinks" in h.lower() or "cocktails" in h.lower() or "side" in h.lower() or "sides" in h.lower():
                        continue
                    else:
                        for menu_item in category_div.findAll("li"):
                            m_i = []
                            for name in menu_item.findAll("span", {"class": "name"}):
                                m_i.append(u' '.join(name).encode('utf-8').strip())
                            for desc in menu_item.findAll("p"):
                                m_i.append(u' '.join(desc).encode('utf-8').strip())
                            if m_i not in menu_items:
                                menu_items.append(m_i)

    # Process alternative menus (breakfast, lunch, dinner, etc.)
    if len(alt_menu_links) > 0:
        for alt_link in alt_menu_links:
            print "Processing alternative menu at: " + str(alt_link)
            time.sleep(randint(0, 60))

            req = urllib2.Request(alt_link, headers=hdr)

            try:
                page = urllib2.urlopen(req)
            except urllib2.HTTPError, e:
                print "Failed on this link: " + link
                sys.exit(1)

            content = page.read()

            soup = BeautifulSoup(content)

            for menu in soup.findAll("div", {"id": "menu"}):
                for category_div in menu.findAll("div", {"class": "category"}):
                    for category_head in category_div.findAll("div", {"class": "category_head"}):
                        for header in category_head.findAll("h3"):
                            h = clean(header.text)
                            if "beverage" in h.lower() or "beverages" in h.lower() or "drink" in h.lower() or "drinks" in h.lower() or "cocktails" in h.lower() or "side" in h.lower() or "sides" in h.lower():
                                continue
                            else:
                                for menu_item in category_div.findAll("li"):
                                    m_i = []
                                    for name in menu_item.findAll("span", {"class": "name"}):
                                        m_i.append(u' '.join(name).encode('utf-8').strip())
                                    for desc in menu_item.findAll("p"):
                                        m_i.append(u' '.join(desc).encode('utf-8').strip())
                                    if m_i not in menu_items:
                                        menu_items.append(m_i)

    # Write the results to a text file within the menus/ directory
    print "Writing menu for: " + company_name
    with open("menus/" + company_name + '.txt', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for m_i in menu_items:
            writer.writerow(m_i)

print "Wrote all menus to file."
