from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    x_coordinate = models.IntegerField()
    y_coordinate = models.IntegerField()
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.name}"


class CityGateNorth(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_gate_north')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.name}"


class CityGateSouth(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_gate_south')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class CityGateEast(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_gate_east')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class CityGateWest(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_gate_west')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class MarketSquare(models.Model):
    name = models.CharField(max_length=100)
    city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='market_square')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class MarketShop(models.Model):
    name = models.CharField(max_length=100)
    market = models.ForeignKey(MarketSquare, on_delete=models.CASCADE, related_name='market_shop')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class CraftsmenSquare(models.Model):
    name = models.CharField(max_length=100)
    city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='craftsmen_square')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Workshop(models.Model):
    name = models.CharField(max_length=100)
    craftsmen_square = models.ForeignKey(CraftsmenSquare, on_delete=models.CASCADE, related_name='workshops')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class PalaceSquare(models.Model):
    name = models.CharField(max_length=100)
    city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='palace_square')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class CityManagement(models.Model):
    name = models.CharField(max_length=100)
    palace_square = models.OneToOneField(PalaceSquare, on_delete=models.CASCADE, related_name='city_management')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class RoyalPalace(models.Model):
    name = models.CharField(max_length=100)
    palace_square = models.OneToOneField(PalaceSquare, on_delete=models.CASCADE, related_name='royal_palace')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class EntertainmentDistrict(models.Model):
    name = models.CharField(max_length=100)
    city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='entertainment_district')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Tavern(models.Model):
    name = models.CharField(max_length=100)
    entertainment_district = models.ForeignKey(EntertainmentDistrict, on_delete=models.CASCADE, related_name='taverns')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Casino(models.Model):
    name = models.CharField(max_length=100)
    entertainment_district = models.ForeignKey(EntertainmentDistrict, on_delete=models.CASCADE, related_name='casinos')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    entertainment_district = models.ForeignKey(EntertainmentDistrict, on_delete=models.CASCADE, related_name='hotels')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name
