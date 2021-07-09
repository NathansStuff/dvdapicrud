from django.contrib import admin
from django.urls import path, include
from dvdapi.views import MyView

from .router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),     # localhost:/api => go to router.py
    path('api/barcode', MyView.as_view()),
]