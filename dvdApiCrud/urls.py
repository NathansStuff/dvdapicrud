from django.contrib import admin
from django.urls import path, include
from dvdapi.views import MyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dvdapi.urls')),     # localhost:/api => go to router.py
    path('api/barcode', MyView.as_view()),
]