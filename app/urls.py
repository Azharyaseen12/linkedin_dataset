from django.contrib import admin
from django.urls import path,include
from .views import home, filter,savesearches,savedsearches,delete_search,dashboard

urlpatterns = [
    path('home/', home , name = 'home'),
    path('', filter , name = 'filter'),
    path('savesearches/', savesearches , name = 'savesearches'),
    path('savedsearches/', savedsearches , name = 'savedsearches'),
    path('delete_search/<int:id>', delete_search , name = 'delete'),
    path('dashboard/', dashboard , name = 'dashboard'),
]
