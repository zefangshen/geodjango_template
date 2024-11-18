from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_vector, name='redirect_to_vector'),
    path('vector/', views.show_vector_data, name='show_vector'),
    # path('raster/', views.show_raster_data, name='show_raster'),
    path('map/', views.show_raster_data, name='show_raster'),
    path('get_raster_tile/', views.get_raster_tile, name='get_raster_tile'),
]