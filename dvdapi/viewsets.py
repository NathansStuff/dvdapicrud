from rest_framework import viewsets
from rest_framework import filters
from . import models
from . import serializers


class DvdViewset(viewsets.ModelViewSet):
    search_fields = ['barcode', 'title']
    filter_backends = (filters.SearchFilter,)      #/?search= now searches!
    queryset = models.Dvd.objects.all()
    serializer_class = serializers.DvdSerializer
