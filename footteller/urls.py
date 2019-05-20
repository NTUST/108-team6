from django.contrib import admin
from django.urls import path

from main.views import players, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('players', players, name="base"),
]
