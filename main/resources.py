from import_export import resources
from .models import *

class UquvchiRes(resources.ModelResource):
    class Meta:
        model = Uquvchi

class SinfRes(resources.ModelResource):
    class Meta:
        model = Sinf

class KitobRes(resources.ModelResource):
    class Meta:
        model = Kitob

class BuyRes(resources.ModelResource):
    class Meta:
        model = Buy
    