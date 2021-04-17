from django.urls import path
from app import views

# using str for string pattern instead of slug as slug doesn't allow spaces
urlpatterns = [
    path('', views.stock_list),
    path('<str:stockname>', views.stock_list_by_name),
]