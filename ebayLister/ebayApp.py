from modules.fileReader import fileReader
from modules.dbSearchCreate import dbSearchCreate
from modules.ebayLister import scrapeLister

# Step 1: Run the script to open new webbrowser instance. Log in.
# chrome.exe -remote-debugging-port=9014 --user-data-dir="C:\Selednium\Chrome_Test_Profile"
# Step 2: Run the database to log the results for later use
# python manage.py runserver

search_terms = fileReader()
custom_label = 'E33'

dbSearchCreate(search_terms)
scrapeLister(search_terms, custom_label)