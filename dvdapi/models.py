from django.db import models


class Dvd(models.Model):
    barcode = models.DecimalField(max_digits=20, decimal_places=0)
    title = models.CharField(max_length=200)
    cexPhotoUrl = models.CharField(max_length=200)
    booktopiaPhotoUrl = models.CharField(max_length=200)
    cexSell = models.DecimalField(max_digits=5, decimal_places=2)
    cexBuy = models.DecimalField(max_digits=5, decimal_places=2)
    cexTrade = models.DecimalField(max_digits=5, decimal_places=2)
