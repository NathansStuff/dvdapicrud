from driver import createDriver
from searchDatabase import searchDatabase
from cex import scrapeCex
from booktopia import scrapeBooktopia
from postData import postData
from createListing import createListing

# Step 1: Run the script to open new webbrowser instance. Log in.
# chrome.exe -remote-debugging-port=9014 --user-data-dir="C:\Selednium\Chrome_Test_Profile"
# Step 2: Run the database to log the results for later use
# python manage.py runserver

# TWO PROCESSES
# One to List on ebay
# One to search for stuff to buy and add to db

def scrapeLister(search_terms, custom_label):
    driver = createDriver()
    warnings = []
    total_search = len(search_terms)

    print(f'Executing {total_search} times')

    count = 0
    for term in search_terms:
        count += 1
        print(f'Status: {count}/{total_search}')

        # 1 - Search database
        dbData = searchDatabase(term)

        # Not already in database
        if str(dbData) == '[]':
            print('Not in database... scraping data')
            # 2 - Scrape cex
            cexData = scrapeCex(driver, term)
            # 2A Unpack cexData
            title = cexData[0]
            cexImageUrl = cexData[1]
            cexSell = cexData[2]
            cexBuy = cexData[3]
            cexTrade = cexData[4]
            warnings.append(cexData[5])

            # 3 - Scrape booktopia
            booktopiaImageUrl = scrapeBooktopia(driver, term)

            # 4 - Post to database
            dbResponse = postData(term, title, cexImageUrl,
                                  booktopiaImageUrl, cexSell, cexBuy, cexTrade)
            if dbResponse.status_code == 201:
                print('Successfully stored data in db')
            else:
                print('Error storing data in database!')
                print(dbResponse)
        else:
            print('Found in database!')
            print(dbData)
            print('*************************')
            title = dbData[0]["title"]
            cexImageUrl = dbData[0]["cexPhotoUrl"]
            booktopiaImageUrl = dbData[0]["booktopiaPhotoUrl"]

        # 5 - Create ebay Listing
        createListing(driver, term, custom_label, title, cexImageUrl, booktopiaImageUrl)
        print('Listing successfully created')
    
    print('*********************************')
    print(f'Job complete! {total_search} items searched and created!')
    print(f'There were {str(len(warnings))} warnings!')
    for warning in warnings:
        print(f'{warning}')