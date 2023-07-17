from django.db import transaction
from game.models.town_model import City, CityGateNorth, CityGateSouth, CityGateEast, CityGateWest, MarketSquare, \
    MarketShop, \
    CraftsmenSquare, Workshop, PalaceSquare, CityManagement, RoyalPalace, EntertainmentDistrict, Tavern, Casino, Hotel
from game.location_model.location_model import Location


def create_sample_city():
    # Создание города
    with transaction.atomic():
        city = City.objects.create(name='Примерный город', x_coordinate=1, y_coordinate=1, description='Это примерный '
                                                                                                       'город')
        # Получение или создание координаты
        location, created = Location.objects.get_or_create(x=city.x_coordinate, y=city.y_coordinate,
                                                           defaults={'name': city.name, 'passable': True})

        # Изменение значения passable, если False
        if not location.passable:
            location.passable = True
            location.save()

        # Связывание координаты с городом
        city.location = location
        city.save()

        # Создание ворот
        CityGateNorth.objects.create(name='Северные ворота', city=city, description='Это северные ворота')
        CityGateSouth.objects.create(name='Южные ворота', city=city, description='Это южные ворота')
        CityGateEast.objects.create(name='Восточные ворота', city=city, description='Это восточные ворота')
        CityGateWest.objects.create(name='Западные ворота', city=city, description='Это западные ворота')

        # Создание площадей и магазинов
        market_square = MarketSquare.objects.create(name='Торговая площадь', city=city,
                                                    description='Это торговая площадь')
        MarketShop.objects.create(name='Магазин 1', market=market_square, description='Это магазин 1')
        MarketShop.objects.create(name='Магазин 2', market=market_square, description='Это магазин 2')

        craftsmen_square = CraftsmenSquare.objects.create(name='Площадь мастеров', city=city,
                                                          description='Это площадь мастеров')
        Workshop.objects.create(name='Мастерская 1', craftsmen_square=craftsmen_square, description='Это мастерская 1')
        Workshop.objects.create(name='Мастерская 2', craftsmen_square=craftsmen_square, description='Это мастерская 2')

        palace_square = PalaceSquare.objects.create(name='Дворцовая площадь', city=city,
                                                    description='Это дворцовая площадь')
        CityManagement.objects.create(name='Управление города', palace_square=palace_square,
                                      description='Это управление города')
        RoyalPalace.objects.create(name='Королевский дворец', palace_square=palace_square,
                                   description='Это королевский дворец')

        # Создание развлекательного района
        entertainment_district = EntertainmentDistrict.objects.create(name='Развлекательный район', city=city,
                                                                      description='Это развлекательный район')
        Tavern.objects.create(name='Таверна', entertainment_district=entertainment_district, description='Это таверна')
        Casino.objects.create(name='Игорный дом', entertainment_district=entertainment_district,
                              description='Это игорный дом')
        Hotel.objects.create(name='Гостиница', entertainment_district=entertainment_district,
                             description='Это гостиница')

    print('Типовой город успешно создан.')

