from bs4 import BeautifulSoup as soup

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

import time

def scrapeCex(driver, searchTerm):
    # Retrive url in headless browser
    driver.get('https://au.webuy.com/')

    # Find search box & enter barcode
    search = driver.find_element_by_id("stext")
    search.send_keys(searchTerm + Keys.RETURN)

    time.sleep(5)
    currentUrl = driver.current_url

    if 'search' in currentUrl:  # If taken to a list, not individual page
        firstResult = driver.find_element_by_xpath('//div[@class="desc"]/h1')
        firstResult.click()
        time.sleep(5)
    
    # Wait for the page to load
    WebDriverWait(driver, 10).until(presence_of_element_located(
        (By.CLASS_NAME, "productInfoImageArea")))

    # Send to soup
    source = driver.page_source
    pageSoup = soup(source, "html.parser")

    # Title
    text = pageSoup.findAll("td", {"class": "productName"})[0].text
    splitText = text.split('★', 1)[0].strip().split('(', 1)[0].strip()
    cexTitleText = splitText + ' | DVD Region 4 (PAL) (Australia) | Free Post'
    # Sell Price
    cexSellPrice = pageSoup.findAll("td", {"id": "Asellprice"})[0].text
    # Cash Price
    cexCashPrice = pageSoup.findAll("span", {"id": "Acashprice"})[0].text
    # Trade Price
    cexTradePrice = pageSoup.findAll("span", {"id": "Aexchprice"})[0].text
    # Image url
    imageDiv = pageSoup.findAll("div", {"class": "productImg"})[
        0].findAll('img', {'alt': 'Product photo'})[0]
    cexImageUrl = str(imageDiv).split('src="', 1)[
        1].split('"/>', 1)[0].replace(" ", "%20")

    print("Title: " + cexTitleText)
    print("Sell Price: " + cexSellPrice)
    print("Buy Price: " + cexCashPrice)
    print("Trade Price: " + cexTradePrice)
    print("Cex URL: " + cexImageUrl)

    cexCashPrice = cexCashPrice.split('$', 1)[1].strip()
    cexTradePrice = cexTradePrice.split('$', 1)[1].strip()
    cexSellPrice = cexSellPrice.split('$', 1)[1].strip()

    warnings = []
    if (float(cexCashPrice) >= 1) or (float(cexTradePrice) >= 1):
        warnings.append('CEX Buys ' + splitText + 'for cash $' +
                        cexCashPrice + ' or trade $' + cexTradePrice)

    cexSell = float(cexSellPrice)
    cexBuy = float(cexCashPrice)
    cexTrade = float(cexTradePrice)
