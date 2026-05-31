from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='home'),
    path('beranda/', views.home, name='beranda'),
    path('recommendation/', views.recommendation_view, name='recommendation'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('register/', views.register, name='register'),
    path('masuk/', views.user_login, name='user_login'),
    path('keluar/', views.user_logout, name='user_logout'),
]