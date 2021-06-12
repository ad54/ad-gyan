from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='idx_search'),
    path('upload-csv', views.import_data, name='import_data'),
    path('export-data', views.export_data, name='export_data'),
    path('analytics', views.get_analytics, name='analytics'),
]