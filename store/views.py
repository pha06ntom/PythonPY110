from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from .models import DATABASE
from django.http import HttpResponse
from logic.services import filtering_category, view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import render


# Create your views here.

def products_view(request):
    if request.method == "GET":
        # Обработка id из параметров запроса
        if id_product := request.GET.get('id'):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get('category')
        if ordering_key := request.GET.get('ordering'):
            if request.GET.get('reverse') in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)

        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


def products_page_view(request, page):
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
        # with open('store/shop.html', encoding="utf-8") as f:
        #     data = f.read()
        # return HttpResponse(data)
        category_key = request.GET.get('category')
        if ordering_key := request.GET.get('ordering'):
            if request.GET.get('reverse') in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)

        return render(request, 'store/shop.html',
                      context={"products": data,
                               "category": category_key})


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]
            product["quantity"] = quantity
            product["price_total"] = f"{quantity * product['price_after']:.2f}"
            products.append(product)
        return render(request, 'store/cart.html', context={"products": products})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "Неудачная попытка добавления товара в корзину"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удален из корзины"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "Неудачная поптыка удаления товара из корзины"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})
