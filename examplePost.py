import requests

payload = {
    'barcode': 231,
    'title': 'test',
    'cexPhotoUrl': 'cex',
    'booktopiaPhotoUrl': 'book',
    'cexSell': 4.98,
    'cexBuy': 5.00,
    'cexTrade': 1
}

r = requests.post('http://127.0.0.1:8000/api/dvd/', data=payload)
