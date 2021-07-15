from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as soup


# Configuring the driver
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("version='87.0.4280.88'")
chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9014')
driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.ebay.com.au/itm/353463612133'
code = url.split('https://www.ebay.com.au/itm/', 1)[1]

driver.get(
    f'https://bulksell.ebay.com.au/ws/eBayISAPI.dll?SingleList&sellingMode=ReviseItem&lineID={code}')


titleField = driver.find_element_by_id('editpane_title')
titlePre = driver.find_element_by_id('editpane_title').get_attribute('value')
title = titlePre.split(' | DVD', 1)[0].strip()

# 80 Characters Max
if len(title) <= 35:
    titleText = title + ' | DVD Region 4 (PAL) (Australia) | Free Post'
elif len(title) <= 37:
    titleText = title + ' | DVD Region 4 (PAL) (Australia) Free Post'

elif len(title) <= 39:
    titleText = title + ' | DVD Region 4 (PAL) Australia Free Post'
else:
    titleText = title + ' | DVD Region 4 (PAL) Free Post'

titleField.clear()
titleField.send_keys(titleText)

itemSpecificTitle = driver.find_element_by_id(
    'Listing.Item.ItemSpecific[Movie/TV Title]')
itemSpecificTitle.clear()
itemSpecificTitle.send_keys(title)


price = driver.find_element_by_id('binPrice')
price.clear()
price.send_keys('6.99')
