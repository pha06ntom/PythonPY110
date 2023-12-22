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
    if os.path.exists('cart.json'): # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    cart = {'product': {}} # Создаем пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f: # Создаем файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart

def add_to_cart(id_product: str):
    """
        Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
        Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

        :param id_product: Идентификационный номер продукта в виде строки.
        :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления (товара по id_product
        не существует).
    """
    cart = view_in_cart()

    if not DATABASE.get(id_product):
        return False

    for product in cart.values():
        if not product.get(id_product):
            product[id_product] = 1
        else:
            product[id_product] += 1
        print(product)
    with open('cart.json', encoding='utf-8') as f:
        json.dump(product, f)




if __name__ == "__main__":
    from store.models import DATABASE
    print(add_to_cart('3'))
