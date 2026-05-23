from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # dashboard
    path('dashboard/', views.dashboard_index, name='dashboard_index'),

    # product
    path('dashboard/products/', views.dashboard_products, name='dashboard_products'),
    path('dashboard/products/add/', views.product_add, name='product_add'),
    path('dashboard/products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('dashboard/products/delete/<int:pk>/', views.product_delete, name='product_delete'),

    # criteria
    path('dashboard/criteria/', views.dashboard_criteria, name='dashboard_criteria'),
    path('dashboard/criteria/add/', views.criteria_add, name='criteria_add'),
    path('dashboard/criteria/edit/<int:pk>/', views.criteria_edit, name='criteria_edit'),
    path('dashboard/criteria/delete/<int:pk>/', views.criteria_delete, name='criteria_delete'),

    # product values
    path('dashboard/values/', views.dashboard_values, name='dashboard_values'),
    path('dashboard/values/add/', views.value_add, name='value_add'),
    path('dashboard/values/edit/<int:pk>/', views.value_edit, name='value_edit'),
    path('dashboard/values/delete/<int:pk>/', views.value_delete, name='value_delete'),
]