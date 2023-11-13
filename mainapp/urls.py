from django.urls import path
from .views import plot_view,run_spider,main,file_list

urlpatterns = [
    path('',main,name='main'),
    path('files/', file_list, name='file_list'),
    path('files/<str:filename>/plot/', plot_view, name='plot_view'),
    path('run_spider/', run_spider, name='run_spider')
]