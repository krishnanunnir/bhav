from django.urls import path
from  . import views

# using str for string pattern instead of slug as slug doesn't allow spaces
urlpatterns = [
    path('stonks', views.stock_list),
    path('search', views.stock_list_by_name),
    path('load', views.load_data),
]