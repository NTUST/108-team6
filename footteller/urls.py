from django.contrib import admin
from django.urls import path

from main.views import base, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('base', base, name="base"),
]
