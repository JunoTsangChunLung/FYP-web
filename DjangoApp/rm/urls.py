from django.urls import path
from . import views

app_name = 'rm'

urlpatterns =[
    path("create-product/", views.create_product, name='create-product'),
    path("add-category/", views.add_cat, name="add-category"),
    path('get-subcategories/', views.get_subcategories, name='get-subcategories'),
    path("optimization/", views.revenue_optimization, name = "optimization")
   ]