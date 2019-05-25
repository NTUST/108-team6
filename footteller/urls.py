from django.contrib import admin
from django.urls import path
from analysis.views import predict,predict_result
from main.views import players, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('players', players, name="base"),
    path('predict/', predict, name="predict"),
    path('analysis_form/', predict_result)
]
