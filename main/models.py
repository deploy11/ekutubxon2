from django.db import models
from users.models import User
from django.urls import reverse
from django.utils.timezone import now
# Create your models here.
class Sinf(models.Model):
    title = models.CharField(max_length=500,verbose_name='Sinf nomi')
    rahbar = models.CharField(max_length=500,verbose_name='Sinf Rahbar')
    date = models.DateTimeField(auto_now_add=True)
    maktab = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('create_sinf')

class Uquvchi(models.Model):
    Ismi = models.CharField(max_length=500,verbose_name='O`quvchi Ismi')
    Familiya = models.CharField(max_length=500,verbose_name='O`quvchi Familiyasi')
    Sharif = models.CharField(max_length=500, verbose_name='O`quvchi Sharif')
    sinf = models.ForeignKey(Sinf,on_delete=models.CASCADE)
    maktab = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.Ismi} {self.Familiya} {self.Sharif} {self.sinf}')

    def get_absolute_url(self):
        return reverse('create_uquvchi')

class Kitob(models.Model):
    title = models.CharField(max_length=500, verbose_name='Kitob nomi')
    yosh = models.CharField(max_length=500, verbose_name='Yosh chegarasi')
    description = models.TextField(verbose_name='Kitob Haqida Malumot')
    author = models.CharField(max_length=500,verbose_name='Kim yozgan')
    year = models.CharField(max_length=500,verbose_name='Kitob chiqan yil')
    maktab = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('create_kitob')

class Buy(models.Model):
    sender = models.ForeignKey(Uquvchi,on_delete=models.CASCADE)
    Kitob = models.ForeignKey(Kitob,on_delete=models.CASCADE)
    vaqt = models.DateField(default=now,verbose_name='Kitob topshirish muddati')
    datess = models.DateField(auto_now=True)
    muddat_otdi = models.BooleanField(default=False)
    finish = models.BooleanField(default=False)
    maktab = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('create_buys')
    
class School(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    formular_soni = models.CharField(max_length=500)
    topshirilgan = models.CharField(max_length=500)
    topshirilmagan = models.CharField(max_length=500)
    jarayonda = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.user.matab
    
Baholar = (
    ('zo`r','zo`r'),
    ('qoniqarli','qoniqarli'),
    ('qoniqarsiz','qoniqarsiz'),
    ('yomon','yomon')
)

class Tekshiruv(models.Model):
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    baho = models.CharField(max_length=500,choices=Baholar)

    def __str__(self) -> str:
        return self.school