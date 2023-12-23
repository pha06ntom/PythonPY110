import json
import os
from store.models import DATABASE


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


def view_in_cart() -> dict:
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json"
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    cart = {'products': {}}  # Создаем пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:  # Создаем файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


def add_to_cart(id_product: str) -> bool:
    """
        Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
        Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

        :param id_product: Идентификационный номер продукта в виде строки.
        :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления (товара по id_product
        не существует).
    """
    cart = view_in_cart()
    initial_value = 1

    if not DATABASE.get(id_product):
        return False

    if cart['products'].get(id_product):
        cart['products'][id_product] += 1
    else:
        cart['products'][id_product] = initial_value

    with open('cart.json', 'w', encoding='utf-8') as f:
        json.dump(cart, f)

    return True


def remove_from_cart(id_product: str) -> bool:
    """
        Удаляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
        с этим продуктом.

        :param id_product: Идентификационный номер продукта в виде строки.
        :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
        не существует).
    """
    cart = view_in_cart()

    if cart['products'].get(id_product):
        del cart['products'][id_product]
    else:
        return False

    with open('cart.json', 'w', encoding='utf-8') as f:
        json.dump(cart, f)

    return True


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
