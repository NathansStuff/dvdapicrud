from rest_framework import viewsets
from . import models
from . import serializers

class DvdViewset(viewsets.ModelViewSet):
    queryset = models.Dvd.objects.all()
    serializer_class = serializers.DvdSerializer