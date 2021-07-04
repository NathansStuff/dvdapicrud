from bs4 import BeautifulSoup as soup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options

import time
import urllib.request
from glob import glob
import os


# Step 1: Run the script to open new webbrowser instance. Log in.
# chrome.exe -remote-debugging-port=9014 --user-data-dir="C:\Selednium\Chrome_Test_Profile"

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
    '9326314015709',
    '9398700026019',
    '9398523225033',
    '9321337173702',
    '9317731056406',
    '9398522127031',
    '5050582781458',
    '5050582566499',
    '9317731057694',
    '9317731042478',
    '9398523280032',
    '9337874001231',
    '9317731041921',
    '9317731004148',
    '9418212007891',
    '9317206031587',
    '9338683006264',
    '9321337068671',
    '9326314013378',
    '9397810199699',
    '9317731003042',
    '5021456171941',
    '9317731127137',
    '5050583010526',
    '9325336125304',
    '9335522035232',
    '9315841999033',
    '5021456171958',
    '9325336016862',
    '9325336011317',
    '9397911243291',
    '9321337042411',
    '725906473795',
    '9321337037615',
    '9317731139963',
    '9326314010742',
    '9398520576039',
    '9398710741094',
    '9326314000989',
    '9398710740899',
    '9324915050587',
    '9324915050044',
    '9398522237037',
    '9315842015169',
    '9398521585030',
    '9317206017581',
    '9397810259096',
    '9324915082236',
    '9337874021390',
    '9317731054716',
    '9325425025102',
    '9337874001262',
    '9398522219033',
    '9398710625691',
    '9325336135532',
    '9398510622036',
    '9418212006856',
    '9398710177190',
    '9337874001590',
    '5050582770179',
    '9317731075742',
    '9398521009031',
    '9397810051393',
    '9317485442388',
    '9321337099149',
    '9398710893298',
    '8717418270582',
    '9324915054455',
    '9418212006467',
    '9320314005210',
]


def createListing(searchTerm, cexTitleText, cexImageUrl, booktopiaImageUrl):

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
    sku.send_keys('E13')

    # Item specifics - DVD Title
    try:
        itemSpecificTitle = driver.find_element_by_id(
            'Listing.Item.ItemSpecific[Movie/TV Title]')
        itemSpecificTitle.clear()
        title = cexTitleText.split(
            ' | DVD Region 4 (PAL) (Australia) | Free Post', 1)[0]
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


def scrapeBooktopia(searchTerm, cexTitleText, cexImageUrl):
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
    createListing(searchTerm, cexTitleText, cexImageUrl, booktopiaImageUrl)


def searchBooktopia(searchTerm, cexTitleText, cexImageUrl):
    # Retrive url in headless browser
    driver.get('https://www.booktopia.com.au/')

    # Find search box & enter barcode
    search = driver.find_element_by_id("header-search-box")
    search.send_keys(searchTerm + Keys.RETURN)

    time.sleep(2)

    scrapeBooktopia(searchTerm, cexTitleText, cexImageUrl)


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

    if (float(cexCashPrice) >= 1) or (float(cexTradePrice) >= 1):
        warnings.append('CEX Buys ' + splitText + 'for cash $' +
                        cexCashPrice + ' or trade $' + cexTradePrice)

    searchBooktopia(searchTerm, cexTitleText, cexImageUrl)


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
    print('-------------ERRORS-------------')
    for error in errors:
        print(error)
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
