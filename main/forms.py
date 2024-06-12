# dwitter/forms.py

from django import forms
from .models import *

class UquvhciForm(forms.ModelForm):
    class Meta:
        model = Uquvchi
        exclude = ("maktab",)

class SinfForm(forms.ModelForm):
    class Meta:
        model = Sinf
        exclude = ("maktab",)

class BuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        exclude = ("maktab",'muddat_otdi','finish')

class KitobForm(forms.ModelForm):
    class Meta:
        model = Kitob
        exclude = ("maktab",)

class TekshirForm(forms.ModelForm):
    class Meta:
        model = Tekshiruv
        exclude = ("maktab",)
