from django.urls import path
from .views import recommendation_view

urlpatterns = [
    path('', recommendation_view, name='recommendation'),
]