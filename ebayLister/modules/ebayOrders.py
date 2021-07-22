from bs4 import BeautifulSoup as soup

from modules.driver import createDriver


def ebayOrders():
    driver = createDriver()
    driver.get('https://www.ebay.com.au/sh/ord/?filter=status:AWAITING_SHIPMENT')

    # Send to soup
    source = driver.page_source
    pageSoup = soup(source, "html.parser")

    # Summary
    orderNum = pageSoup.findAll("span", {"id": "summaryText"})[0].text.split('of ', 1)[1]
    print(f'There are {orderNum} orders')
    moneyTotal = pageSoup.findAll("span", {"class": "totals--container"})[0].text.split('AU ', 1)[1].split('Chart',1)[0]
    print(f'Total value: {moneyTotal}')

    # Orders
    orders = pageSoup.findAll("span", {"class": "user-name"})
    seen = set()
    uniq = []
    duplicates = []
    for order in orders:
        if order not in seen:
            uniq.append(order)
            seen.add(order)
        else:
            duplicates.append(order)
    if len(duplicates) != 0:
        print(f'There are {len(duplicates)} multi order customers.')
        for dup in duplicates:
            print(f'{dup.text} has multiple orders')
    
    # Items sold
    items = pageSoup.findAll("td", {"class": "order-purchase-details"})
    print(f'Items sold: {len(items)}')

    itemList = []
    for item in items:
        itemTitle = item.findAll("span", {"class": "item-title"})[0].text
        itemSku = item.findAll("span", {"class": "item-custom-sku-pair"})[0].text.split('Custom label (SKU): ',1)[1]
        itemChoice = ''
        try: 
            itemChoice = item.findAll("span", {"class": "variation-pair"})[0].text.split('Choice:',1)[1]
        except:
            pass
        itemDets = itemSku + ': ' + itemTitle + itemChoice
        itemList.append(itemDets)
    sortedItems = sorted(itemList)
    for elem in sortedItems:
        print(elem)