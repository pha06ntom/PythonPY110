from django.urls import path
from .views import product_view, shop_view, product_page_view

urlpatterns = [
    path('product/', product_view),
    path('', shop_view),
    path('product/<slug:page>.html', product_page_view),
    path('product/<int:page>', product_page_view),
]
