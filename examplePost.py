import requests

payload = {
    'barcode': 3233,
    'title': 'Ice Runner, The',
    'cexPhotoUrl': 'https://au.static.webuy.com/product_images/DVD/DVD%20Movies/9326314015709_l.jpg',
    'booktopiaPhotoUrl': '',
    'cexSell': 4.98,
    'cexBuy': 5.00,
    'cexTrade': 1
}

r = requests.post('http://127.0.0.1:8000/api/dvd/', data=payload)
print(r)