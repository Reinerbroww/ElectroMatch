from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommendation/', views.recommendation_view, name='recommendation'),
]