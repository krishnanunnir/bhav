from django.urls import path
from app import views

# using str for string pattern instead of slug as slug doesn't allow spaces
urlpatterns = [
    path('stonks', views.stock_list),
    path('search', views.render_stock),
    path('<str:stockname>', views.stock_list_by_name),
    path('downloads/', views.get_as_zip),
    path('downloads/<str:stockname>', views.get_as_zip),
]