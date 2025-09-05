from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import render
from .models import Product
from .permissions import IsVendor, IsVendorOwner
from rest_framework import generics, permissions, filters


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsVendor]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)


class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOwner]


# Vendor can create products
# class ProductCreateView(generics.CreateAPIView):
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         if self.request.user.role != "vendor":
#             raise PermissionDenied("Only vendors can create products.")
#         serializer.save(vendor=self.request.user)


# # Vendor can update/delete only their products
# class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_update(self, serializer):
#         if self.request.user != self.get_object().vendor:
#             raise PermissionDenied("You can only edit your own products.")
#         serializer.save()

#     def perform_destroy(self, instance):
#         if self.request.user != instance.vendor:
#             raise PermissionDenied("You can only delete your own products.")
#         instance.delete()


# Customers & Vendors can view/search products
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # search_fields = ["name", "description"]
    # ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


def product_list_page(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})
