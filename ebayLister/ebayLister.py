from driver import createDriver
from searchDatabase import searchDatabase

# Step 1: Run the script to open new webbrowser instance. Log in.
# chrome.exe -remote-debugging-port=9014 --user-data-dir="C:\Selednium\Chrome_Test_Profile"
# Step 2: Run the database to log the results for later use
# python manage.py runserver

search_terms = [
    '9326314015709',
]


def scrapeLister(search_terms):
    driver = createDriver()
    errors = []
    warnings = []
    total_search = len(search_terms)

    print(f'Executing {total_search} times')

    count = 0
    for term in search_terms:
        count += 1
        print(f'Status: {count}/{total_search}')

        # 1 - Search database
        dbData = searchDatabase(term)
        if dbData == '[]':
            # Make new listing
            print('new listing time!')
        else:
            print(dbData)
        # 2 - Scrape cex
        # 3 - Scrape booktopia
        # 4 - Post to database
        # 5 - Create ebay


scrapeLister(search_terms)
