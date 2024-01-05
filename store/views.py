from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from .models import DATABASE
from django.http import HttpResponse
from logic.services import filtering_category, view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


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
                    return render(request, "store/product.html", context={"product": data})
                    # with open(f'store/products/{page}.html', encoding="utf-8") as file:
                    #     data_product = file.read()
                    # return HttpResponse(data_product)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                return render(request, "store/product.html", context={"product": data})
                # with open(f'store/products/{data["html"]}.html', encoding="utf-8") as file:
                #     product = file.read()
                # return HttpResponse(product)

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


@login_required(login_url='login:login_view')
def cart_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]
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


@login_required(login_url='login:login_view')
def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "Неудачная попытка добавления товара в корзину"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удален из корзины"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "Неудачная поптыка удаления товара из корзины"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})


def coupon_check_view(request, name_coupon):
    """
    Функция реализации проверки действия купона
    """
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        if name_coupon in DATA_COUPON:
            return JsonResponse({"discount": DATA_COUPON[name_coupon]["value"],
                                 "is_valid": DATA_COUPON[name_coupon]["is_valid"]})
        return HttpResponseNotFound("Неверный купон")


def delivery_estimate_view(request):
    """
    Функция реализации расчета стоимости доставки
    """
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 80},
            "fix_price": 100,
        }
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if country in DATA_PRICE:
            if city in DATA_PRICE[country]:
                return JsonResponse({"price": DATA_PRICE[country][city]["price"]})
            else:
                return JsonResponse({"price": DATA_PRICE[country]["fix_price"]})
        return HttpResponseNotFound("Неверные данные")


@login_required(login_url='login:login_view')
def cart_buy_now_view(request, id_product):
    """
    Функция для добавления товара с переходом в корзину
    """
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return redirect("store:cart_view")
            # return cart_view(request)

        return HttpResponseNotFound("Неудачное добавление в корзину")


def cart_remove_view(request, id_product):
    """
    Функция реализации удаления продуктов из корзины
    """
    if request.method == "GET":
        result = remove_from_cart(request, id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound("Неудачное удаление из корзины")
