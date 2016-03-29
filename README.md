# MenuScraper
Anaphylaxis is a serious allergic reaction that is rapid in onset and may cause death. With more careful preventative measures, decreasing the occurrence of these episodes becomes more realistic. Being aware of problematic menu items containing anaphylaxis "triggers" is an important first step in precautionary measures. The purpose of this project is to visit the allmenus.com website and retrieve the contents of each restaurant's menu.

This project is composed of three scripts that each perform a separate function:
1. grab_links_server.py - this script will visit the URLs provided as a variable and collect all of the URLs associated with separate menus on the allmenus.com website
2. menu_scrape_server.py - this script will visit the URLs gathered in the previous script and save each restaurant's menu as a separate text file wihin the menus directory
3. create_categorical_matrix.py - using the triggers.csv and triggers.txt files, this script will aggregate the menus contatined in the menus directory into a matrix. If the menu item description contains an anaphylaxis-causing ingredient, a 0 will appear in that column of ingredient and 1 otherwise. This is to assist with machine learning input.
