import requests
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat, lon: int) -> dict:
    """
    Функция возвращает данные о текущей погоде в населенном пункте, который соотвествует заданным координатам


    Args:
        lat: широта населенного пункта (в градусах): число.
        lon: долгота населенного пункта(в градусах): число.

    Returns:
        Возвращает следующие данные:
        city - населенный пункт, который соответсвует заданным координатам;
        time - время последнего обновления погодных данных (формат час:мин);
        temp - температура (градус Цельсия);
        feel_like_temp - ощущаемая температура (градус Цельсия);
        pressure - давление (мм. ртутного столба);
        humidity - влажность (%);
        wind_speed - скорость ветра (м/с);
        wind_gust - порывы ветра (м/с);
        wind_dir - направление ветра.
    """
    token = 'a6852a23-1d66-44b7-9dfd-fe1680c6e702'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"  # Если вдруг используете тариф «Погода на вашем сайте»
    # то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Данная реализация приведена для тарифа «Тестовый», если у вас Тариф «Погода на вашем сайте», то закомментируйте пару строк указанных ниже
    result = {
        'city': data['geo_object']['locality']['name'],
        # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        'time': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),
        # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        'temp': data['fact']['temp'],
        'feels_like_temp': data['fact']['feels_like'],
        'pressure': data['fact']['pressure_mm'],
        'humidity': data['fact']['humidity'],
        'wind_speed': data['fact']['wind_speed'],
        'wind_gust': data['fact']['wind_gust'],
        'wind_dir': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),
        # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
    }
    return result


def current_weather_api(lat, lon: int) -> dict:
    """
    Функция возвращает данные о текущей погоде в населенном пункте, который соотвествует заданным координатам.
    Иформация о погодных данных запрашивается на сервисе https://www.weatherapi.com/


    Args:
        lat: широта населенного пункта (в градусах): число.
        lon: долгота населенного пункта(в градусах): число.

    Returns:
        Возвращает следующие данные:
        city - населенный пункт, который соответсвует заданным координатам;
        time - время последнего обновления погодных данных (формат час:мин);
        temp - температура (градус Цельсия);
        feel_like_temp - ощущаемая температура (градус Цельсия);
        pressure - давление (мм. ртутного столба);
        humidity - влажность (%);
        wind_speed - скорость ветра (м/с);
        wind_gust - порывы ветра (м/с);
        wind_dir - направление ветра.
    """
    token = 'c34f2557a7134e5bb9f172019230812'
    url = f"https://api.weatherapi.com/v1/current.json?key={token}&q={lat},{lon}"
    response = requests.get(url)
    data = response.json()

    # Преобразование единиц измерения погодных данных

    pressure = round(data['current']['pressure_mb'] * 0.75, 1)  # Перевод давления из ГПа в мм.рт.ст., для этого
    # значение умножается на 0,75. Результат округляется до 1 знака после запятой.
    windSpeed = round(data['current']['wind_kph']/3.6, 1)  # Перевод скорости из км/ч в м/с, для этого значение
    # умножается на 3.6. Результат округляется до 1 знака после запятой.
    windGust = round(data['current']['gust_kph']/3.6, 1)  # Перевод скорости из км/ч в м/с, для этого значение
    # умножается на 3.6. Результат округляется до 1 знака после запятой.

    result = {
        'city': data['location']['name'],
        'time': data['current']['last_updated'],
        'temp': data['current']['temp_c'],
        'feels_like_temp': data['current']['feelslike_c'],
        'pressure': pressure,
        'humidity': data['current']['humidity'],
        'wind_speed': windSpeed,
        'wind_gust': windGust,
        'wind_dir': data['current']['wind_dir'],
    }
    return result


if __name__ == "__main__":
    print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга (погодные данные с сервиса
    # Яндекс.Погода)
    print(current_weather_api(59.93, 30.31)) # Погоднаые данные с сервиса weather api
