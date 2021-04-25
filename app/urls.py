from django.urls import path
from app import views

# using str for string pattern instead of slug as slug doesn't allow spaces
urlpatterns = [
    path('', views.render_stock),
    path('downloads/', views.get_as_csv),
    path('downloads/<str:stockname>', views.get_as_csv),
]