import json
import os
from store.models import DATABASE
from django.contrib.auth import get_user


def filtering_category(database: dict,
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    """
       Функция фильтрации данных по параметрам

       :param database: База данных.
       :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
       :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
       :param reverse: [Опционально] Выбор направления сортировки:
           False - сортировка по возрастанию;
           True - сортировка по убыванию.
       :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
       то возвращается пустой список
       """

    if category_key:
        result = [product for product in database.values() if category_key == product['category']]
    else:
        result = list(database.values())
    if ordering_key:
        result.sort(key=lambda x: x[ordering_key], reverse=reverse)
    return result


def view_in_cart(request) -> dict:
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json"
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username # Получение авторизированного пользователя
    cart = {user: {'products': {}}}  # Создаем пустую корзину для конкретного пользователя
    with open('cart.json', mode='x', encoding='utf-8') as f:  # Создаем файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


def add_to_cart(request, id_product: str) -> bool:
    """
        Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
        Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

        :param id_product: Идентификационный номер продукта в виде строки.
        :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления (товара по id_product
        не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]

    if not DATABASE.get(id_product):
        return False

    if cart['products'].get(id_product):
        cart['products'][id_product] += 1
    else:
        cart['products'][id_product] = 1

    with open('cart.json', 'w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    return True


def remove_from_cart(requset, id_product: str) -> bool:
    """
        Удаляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
        с этим продуктом.

        :param id_product: Идентификационный номер продукта в виде строки.
        :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
        не существует).
    """
    cart_users = view_in_cart(requset)
    cart = cart_users[get_user(requset).username]

    if cart['products'].get(id_product):
        del cart['products'][id_product]
    else:
        return False

    with open('cart.json', 'w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    return True

def add_user_to_cart(request, username: str) -> None:
    """
        Добавляет пользователя в базу данных корзины, если его там не было.

        :param username: Имя пользователя
        :return: None
    """
    cart_users = view_in_cart(request) # Чтение всей базы корзин

    cart = cart_users.get(username) # Получение корзины конкретного пользователя

    if not cart:  # Если пользователя не было в корзине, то создаем его и записываем в базу
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)


def view_in_wishlist(request) -> dict:
    """
    Просматривает содержимое wishlist.json

    :return: Содержимое 'wishlist.json"
    """
    if os.path.exists('wishlist.json'):  # Если файл существует
        with open('wishlist.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username # Получение авторизированного пользователя
    wishlist = {user: {'products': []}}  # Создаем пустой список избранных продуктов для конкретного пользователя
    with open('wishlist.json', mode='x', encoding='utf-8') as f:  # Создаем файл и записываем туда избранные продукты
        json.dump(wishlist, f)

    return wishlist


def add_to_wishlist(request, id_product: str) -> bool:
    """
        Добавляет продукт в избранное.

        :param id_product: Идентификационный номер продукта в виде строки.
        :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления (товара по id_product
        не существует).
    """
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]

    if not DATABASE.get(id_product):
        return False

    if id_product not in wishlist['products']:
        wishlist['products'].append(id_product)

    with open('wishlist.json', 'w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)

    return True


def remove_from_wishlist(request, id_product: str) -> bool:
    """
        Удаляет позицию продукта из избранного.

        :param id_product: Идентификационный номер продукта в виде строки.
        :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
        не существует).
    """
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]

    if id_product in wishlist['products']:
        wishlist['products'].remove(id_product)

    with open('wishlist.json', 'w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)

    return True

def add_user_to_wishlist(request, username: str) -> None:
    """
        Добавляет пользователя в базу данных избранного, если его там не было.

        :param username: Имя пользователя
        :return: None
    """
    wishlist_users = view_in_wishlist(request) # Чтение всей базы

    wishlist = wishlist_users.get(username) # Получение избранного конкретного пользователя

    if not wishlist:  # Если пользователя не было в избранном, то создаем его и записываем в базу
        with open('wishlist.json', mode='w', encoding='utf-8') as f:
            wishlist_users[username] = {'products': []}
            json.dump(wishlist_users, f)




if __name__ == "__main__":
    from store.models import DATABASE

    print(view_in_cart())  # {'products': {}}
    print(add_to_cart('1'))  # True
    print(add_to_cart('0'))  # False
    print(add_to_cart('1'))  # True
    print(add_to_cart('2'))  # True
    print(view_in_cart())  # {'products': {'1': 2, '2': 1}}
    print(remove_from_cart('0'))  # False
    print(remove_from_cart('1'))  # True
    print(view_in_cart())
    print(view_in_wishlist())
    print(add_to_wishlist('1'))  # True
    print(add_to_wishlist('0'))  # False
    print(add_to_wishlist('1'))  # True
    print(add_to_wishlist('2'))  # True
    print(view_in_wishlist())
    print(remove_from_wishlist('0'))  # False
    print(remove_from_wishlist('1'))  # True
    print(view_in_wishlist())
