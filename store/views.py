from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from .models import DATABASE
from django.http import HttpResponse


# Create your views here.
def product_view(request):
    if request.method == "GET":
        id_product = request.GET.get('id')

        if id_product is None:
            data = DATABASE
        elif id_product in DATABASE:
            data = DATABASE[id_product]
        else:
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    with open(f'store/products/{page}.html', encoding="utf-8") as file:
                        data_product = file.read()
                    return HttpResponse(data_product)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'store/products/{data["html"]}.html', encoding="utf-8") as file:
                    product = file.read()
                return HttpResponse(product)

        return HttpResponse(status=404)


def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()
        return HttpResponse(data)
