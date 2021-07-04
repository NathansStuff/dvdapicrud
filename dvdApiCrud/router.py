from dvdapi.viewsets import DvdViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('dvd', DvdViewset)

#