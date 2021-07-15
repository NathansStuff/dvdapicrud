from modules.driver import createDriver
from modules.searchDatabase import searchDatabase
from modules.cex import scrapeCex
from modules.booktopia import scrapeBooktopia
from modules.postData import postData


def dbSearchCreate(search_terms):
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
            try:
                # 2 - Scrape cex
                cexData = scrapeCex(driver, term)
                # 2A Unpack cexData
                title = cexData[0]
                cexImageUrl = cexData[1]
                cexSell = cexData[2]
                cexBuy = cexData[3]
                cexTrade = cexData[4]
                if str(cexData[5]) != '[]':
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
            except:
                print('Unable to scrape ebay')
        else:
            print('Found in database!')
            print(dbData)

    print('*********************************')
    print(f'Job complete! {total_search} items searched!')
    print(f'There were {str(len(warnings))} warnings!')
    for warning in warnings:
        print(f'{warning}')
