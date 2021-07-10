from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.keys import Keys
import time

def scrapeBooktopia(driver, searchTerm):
    # Retrive url in headless browser
    driver.get('https://www.booktopia.com.au/')

    # Find search box & enter barcode
    search = driver.find_element_by_id("header-search-box")
    search.send_keys(searchTerm + Keys.RETURN)

    time.sleep(2)

    # Send to soup
    source = driver.page_source
    pageSoup = soup(source, "html.parser")

    booktopiaImageUrl = ''

    try:
        imageDiv = pageSoup.findAll("div", {"id": "image"})[
            0].findAll('img', {'class': 'lazyload b-trigger loaded'})[0]
        booktopiaImageUrl = str(imageDiv).split('data-image="', 1)[
            1].split('"', 1)[0]

    except:
        print('No booktopia results')

    print('Booktopia Url: ' + booktopiaImageUrl)

    return booktopiaImageUrl