from django.forms import SlugField
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
# from store.models.store.product import Product


# def single_product(request: HttpRequest, slug: SlugField) -> HttpResponse:
#     product = get_object_or_404(Product, slug=slug)
#     return render(request, "website/pages/product-single.html", {"product": product})
