from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Avg

from django.db.models import Count

# from store.models.base.website_config import WebsiteConfig
# from store.models.store.category import Category
# from store.models.store.subcategory import Subcategory


# def get_products_per_page(default: int = 6) -> int:
#     website_config = WebsiteConfig.objects.first()
#     return website_config.products_per_page if website_config else default


# #! Add dedicated pages for category and subcategory
# def filter_by_category(request: HttpRequest, products):
#     subcategory_slug = request.GET.get("subcategory")
#     category_slug = request.GET.get("category")

#     if subcategory_slug:
#         subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
#         products = products.filter(subcategory=subcategory)

#     elif category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)

#     return products


# # ? /products
# def sort_products(request: HttpRequest, products):
#     sort = request.GET.get("sort") or "low_high"
#     # products = Product.objects.all()

#     if sort == "az":
#         products = products.order_by("title")
#     elif sort == "low_high":
#         products = products.order_by("price")
#     elif sort == "high_low":
#         products = products.order_by("-price")

#     products = products.filter(is_active=True).annotate(
#         review_count=Count("reviews"),
#         average_rating=Avg("reviews__rating"),
#     )

#     for product in products:
#         avg = product.average_rating
#         if avg is None:
#             product.int_part = 0  # type: ignore
#             product.decimal_part = 0  # type: ignore
#         else:
#             product.int_part = int(avg)  # type: ignore
#             product.decimal_part = int(round((avg - int(avg)) * 10))  # type: ignore

#     return products
