from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from django.db.models import Count, Avg

from django.core.paginator import Paginator

from django.db.models import Count
# from store.config.pages import webpages

# from store.models import Product
# from store.models.store.category import Category
# from store.models.store.subcategory import Subcategory

# from store.views.view_helpers import filter_by_category, sort_products, get_products_per_page


# Complex Pages
# def home(request: HttpRequest) -> HttpResponse:
#     featured_subcategories = Subcategory.objects.filter(is_featured=True)
#     featured_products = Product.objects.filter(
#         is_featured=True, is_active=True
#     ).annotate(
#         review_count=Count("reviews"),
#     )

#     return render(
#         request,
#         "website/pages/home.html",
#         {
#             "featured_subcategories": featured_subcategories,
#             "featured_products": featured_products,
#             "webpages": webpages,
#         },
#     )


# ? /products
# def products(request: HttpRequest) -> HttpResponse:
#     all_products = Product.objects.all()
#     filtered_products = filter_by_category(request, all_products)
#     sorted_products = sort_products(request, filtered_products)

#     # ? pagination
#     products_per_page = get_products_per_page()
#     paginator = Paginator(sorted_products, products_per_page)
#     page_number = request.GET.get("page")
#     paginated_products = paginator.get_page(page_number)

#     categories = Category.objects.annotate(product_count=Count("products")).filter(
#         product_count__gt=0
#     )
#     subcategories = Subcategory.objects.annotate(
#         product_count=Count("products")
#     ).filter(product_count__gt=0)

#     return render(
#         request,
#         "website/pages/products.html",
#         {
#             "products": sorted_products,
#             "products_page": paginated_products,
#             "categories": categories,
#             "subcategories": subcategories,
#         },
#     )
