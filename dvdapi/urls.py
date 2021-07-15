from .viewsets import DvdViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('dvd', DvdViewset)
# router.register('view', MyView)

urlpatterns = router.urls