from bs4 import BeautifulSoup as soup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options
import requests

import time
import urllib.request
from glob import glob
import os


# Step 1: Run the script to open new webbrowser instance. Log in.
# chrome.exe -remote-debugging-port=9014 --user-data-dir="C:\Selednium\Chrome_Test_Profile"
# Step 2: Run the database to log the results for later use
# python manage.py runserver

# Configuring the driver
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("version='87.0.4280.88'")
chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9014')
webdriver = webdriver.Chrome(options=chrome_options)
driver = webdriver
barcode = ''
url = 'https://au.webuy.com/'

# Retrive url in headless browser
# webdriver.get(url)

##############
# Parameters
##############

number_of_images = 1
GET_IMAGE_TIMEOUT = 2
SLEEP_BETWEEN_INTERACTIONS = 0.1
SLEEP_BEFORE_MORE = 5
output_path = "C:/Users/Noddy/Downloads/Script"

errors = []
warnings = []

search_terms = [
    '9317731086793',
    '5050582782516',
    '9397810148598',
    '9321337052786',
    '9317731058967',
    '9317731062131',
    '9398710602890',
    '9321337038841',
    '3259190237490',
    '9325336029169',
    '9321337040097',
    '9398522779032',
    '9338683000972',
    '9324915091146',
    '9322225088344',
    '9321337164113',
    '9398512977233',
    '9398520198033',
    '9317206015280',
    '5050582566505',
    '9397910896795',
    '9325336189795',
    '9325336012116',
    '033937038457',
    '9398710409291',
    '9321337088594',
    '9338683000521',
    '9325336017593',
    '5050582082333',
    '9397910781091',
    '9318500063779',
    '9325336013489',
    '9326314002976',
    '9398521051030',
    '9398711466897',
    '9325425011440',
    '9326314002976',
]


def storeData(searchTerm, title, cexImageUrl, booktopiaImageUrl, cexSell, cexBuy, cexTrade):

    payload = {
        'barcode': int(searchTerm),
        'title': title,
        'cexPhotoUrl': cexImageUrl,
        'booktopiaPhotoUrl': booktopiaImageUrl,
        'cexSell': cexSell,
        'cexBuy': cexBuy,
        'cexTrade': cexTrade
    }

    requests.post('http://127.0.0.1:8000/api/dvd/', data=payload)


def createListing(searchTerm, cexTitleText, cexImageUrl, booktopiaImageUrl, cexSell, cexBuy, cexTrade):

    # Open ebay listing page
    url = 'https://bulksell.ebay.com.au/ws/eBayISAPI.dll?SingleList&&DraftURL=https://www.ebay.com.au/sh/lst/drafts&ReturnURL=https://www.ebay.com.au/sh/lst/drafts&sellingMode=AddItem&templateId=6123526019'
    driver.get(url)

    # Create Title
    title = driver.find_element_by_id('editpane_title')
    title.send_keys(str(cexTitleText))

    # Send barcode
    sku = driver.find_element_by_id('upc')
    sku.send_keys(str(searchTerm))

    # Click out of barcode
    barcode = driver.find_element_by_id('editpane_skuNumber')
    barcode.send_keys('B3-5')
    time.sleep(10)

    # Ebay forgets SKU as it populates from barcode; resend SKU
    sku = driver.find_element_by_id('editpane_skuNumber')
    sku.send_keys('E33')

    title = cexTitleText.split(
        ' | DVD Region 4 (PAL) (Australia) | Free Post', 1)[0]

    # Item specifics - DVD Title
    try:
        itemSpecificTitle = driver.find_element_by_id(
            'Listing.Item.ItemSpecific[Movie/TV Title]')
        itemSpecificTitle.clear()
        itemSpecificTitle.send_keys(title)
    except:
        print('')

    # ---Photo---1
    # Select the right mini-screen
    iframes = driver.find_elements_by_tag_name('iframe')
    driver.switch_to.frame(iframes[2])
    # Click button with JS
    driver.execute_script(
        "document.getElementsByClassName('copyWebLink2')[0].click();")
    # Enter Photo URl
    urlField = driver.find_element_by_xpath(
        '//ol[@id="cw-inpList"]/li/label/input')
    urlField.send_keys(str(cexImageUrl))
    # Click upload button with JS
    driver.execute_script(
        "document.getElementsByClassName('btn btn-prim btn-m')[1].click();")
    driver.switch_to.default_content()  # Exit iframe
    time.sleep(3)

    if booktopiaImageUrl != '':
        # Photo 2
        # Select the right mini-screen
        iframes = driver.find_elements_by_tag_name('iframe')
        driver.switch_to.frame(iframes[2])
        # Click button with JS
        driver.execute_script(
            "document.getElementsByClassName('copyWebLink2')[0].click();")
        # Enter Photo URl
        urlField = driver.find_element_by_xpath(
            '//ol[@id="cw-inpList"]/li/label/input')
        urlField.send_keys(str(booktopiaImageUrl))
        # Click upload button with JS
        driver.execute_script(
            "document.getElementsByClassName('btn btn-prim btn-m')[1].click();")
        driver.switch_to.default_content()  # Exit iframe
        time.sleep(3)

    # Save Draft
    driver.execute_script("""
        document.querySelectorAll("input[value='Save as draft']")[0].click();
        """)
    time.sleep(3)

    storeData(searchTerm, title, cexImageUrl,
              booktopiaImageUrl, cexSell, cexBuy, cexTrade)


def scrapeBooktopia(searchTerm, cexTitleText, cexImageUrl, cexSell, cexBuy, cexTrade):
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
    createListing(searchTerm, cexTitleText, cexImageUrl,
                  booktopiaImageUrl, cexSell, cexBuy, cexTrade)


def searchBooktopia(searchTerm, cexTitleText, cexImageUrl, cexSell, cexBuy, cexTrade):
    # Retrive url in headless browser
    driver.get('https://www.booktopia.com.au/')

    # Find search box & enter barcode
    search = driver.find_element_by_id("header-search-box")
    search.send_keys(searchTerm + Keys.RETURN)

    time.sleep(2)

    scrapeBooktopia(searchTerm, cexTitleText, cexImageUrl,
                    cexSell, cexBuy, cexTrade)


def scrapeCex(searchTerm):
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

    if (float(cexCashPrice) >= 1) or (float(cexTradePrice) >= 1):
        warnings.append('CEX Buys ' + splitText + 'for cash $' +
                        cexCashPrice + ' or trade $' + cexTradePrice)

    cexSell = float(cexSellPrice)
    cexBuy = float(cexCashPrice)
    cexTrade = float(cexTradePrice)

    searchBooktopia(searchTerm, cexTitleText, cexImageUrl,
                    cexSell, cexBuy, cexTrade)


def searchCex(searchTerm):
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

    scrapeCex(searchTerm)


def summaryPrintOut():
    print('***********************************************')
    print('-------------SUMMARY OF OPERATIONS-------------')
    print('There are ' + str(len(errors)) + ' errors')
    print('There are ' + str(len(warnings)) + ' warnings')
    print('***********************************************')
    print('-------------WARNINGS-------------')
    for warning in warnings:
        print(warning)


print('Executing ' + str(len(search_terms)) + ' Times')
count = 0
for term in search_terms:
    count += 1
    print('Status: ' + str(count) + '/' + str(len(search_terms)))
    try:
        searchCex(
            term
        )
    except Exception:
        print('Error with barcode: ' + term)
        errors.append('Error with barcode ' + term)

summaryPrintOut()
