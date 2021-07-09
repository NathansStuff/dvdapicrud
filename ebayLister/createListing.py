import time

from .postData import postData

def createListing(driver, searchTerm, cexTitleText, cexImageUrl, booktopiaImageUrl, cexSell, cexBuy, cexTrade):

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