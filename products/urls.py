from django.urls import path
from .views import (
    ProductCreateView,
    ProductUpdateDeleteView,
    ProductListView,
    ProductDetailView,
    product_list_page,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("create/", ProductCreateView.as_view(), name="product-create"),
    path("<int:pk>/edit/", ProductUpdateDeleteView.as_view(), name="product-edit"),
    path("page/", product_list_page, name="product-list-page"),
]
