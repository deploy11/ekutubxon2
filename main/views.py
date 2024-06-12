from datetime import date
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib import messages
from tablib import Dataset
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX
from .resources import *
# Create your views here.
@login_required(login_url='login')
def Home(request):
    if request.user.type == 'maktab':
        return HttpResponseRedirect('maktab')
    elif request.user.type == 'tekshiruvchi':
        return HttpResponseRedirect(reverse('tekshiruv'))
    return HttpResponse('home')

@login_required(login_url='login')
def Dashboard_Maktab(request):
    id = request.user
    today = date.today()
    buys_count = Buy.objects.filter(maktab=id).count()
    buys_topshirilmagan_count = Buy.objects.filter(maktab=id,muddat_otdi=True).count()
    buys_topshirilgan_count = Buy.objects.filter(maktab=id,finish=True).count()
    kitoblar_count = Kitob.objects.filter(maktab=id).count()
    buys = Buy.objects.filter(maktab=id,)
    print(buys)

    if School.objects.filter(user=id):
        School.objects.filter(user=id).update(
            user = id,
            formular_soni = buys_count,
            topshirilgan = buys_topshirilmagan_count,
            topshirilmagan = buys_topshirilgan_count,
            jarayonda = Buy.objects.filter(muddat_otdi=False,finish=False).count()
        )
    else:
        School.objects.create(
            user = id,
            formular_soni = buys_count,
            topshirilgan = buys_topshirilmagan_count,
            topshirilmagan = buys_topshirilgan_count,
            jarayonda = Buy.objects.filter(muddat_otdi=False,finish=False).count()
        )
    all_buys = Buy.objects.all()
    for buy in all_buys:
        if buy.vaqt == timezone.now().date():
            buy.muddat_otdi = True
            buy.save()
    con = {
        'buys_count':buys_count,
        'buys_topshirilmagan_count':buys_topshirilmagan_count,
        'buys_topshirilgan_count':buys_topshirilgan_count,
        'kitoblar_count':kitoblar_count,
        'buys':buys
    }
    return render(request,'korish/maktab.html',con)
@login_required(login_url='login')
def finish_formuliyar(request,id):
    buy = Buy.objects.get(id=id)
    if buy.muddat_otdi == True:
        messages.error(request,'Bu Formularning Muddati O`tgan')
    else:
        buy.finish = True
        buy.save()
        messages.success(request,'Jarayon Muvaqiatli Bajarildi')
    return HttpResponseRedirect(reverse('create_buys'))
# ko`rish
@login_required(login_url='login')
def Formulayrs(request):
    id = request.user
    buys = Buy.objects.filter(maktab=id)
    con = {
        'buys':buys,
    }
    return render(request,'korish/formulars.html',con)

@login_required(login_url='login')
def Topshirilgan(request):
    id = request.user
    buys = Buy.objects.filter(maktab=id,finish=True)
    con = {
        'buys':buys,
    }
    return render(request,'korish/topshirilgan.html',con)

@login_required(login_url='login')
def Topshirilmagan(request):
    id = request.user
    buys = Buy.objects.filter(maktab=id,muddat_otdi=True)
    con = {
        'buys':buys,
    }
    return render(request,'korish/topshirilmagan.html',con)

@login_required(login_url='login')
def Kitoblar(request):
    id = request.user
    Books= Kitob.objects.filter(maktab=id)
    con = {
        'books':Books,
    }
    return render(request,'korish/kitoblar.html',con)
# creates
@login_required(login_url='login')
def CreateUquvchi(request):
    id = request.user
    form = UquvhciForm()
    sinf = Sinf.objects.filter(maktab=request.user)
    uquvchi = Uquvchi.objects.filter(maktab=id)
    if request.method == "POST":
        form = UquvhciForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.maktab = request.user
            dweet.save()
    return render(request,'crud/oquvchi.html',{'form':form,'uquvchi':uquvchi,'sinf':sinf})

@login_required(login_url='login')
def CreateSinf(request):
    id = request.user
    form = SinfForm()
    sinf = Sinf.objects.filter(maktab=id)
    if request.method == "POST":
        form = SinfForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.maktab = request.user
            dweet.save()
    return render(request,'crud/sinf.html',{'form':form,'sinf':sinf})

@login_required(login_url='login')
def CreateBuy(request):
    id = request.user
    form = BuyForm()
    buys = Buy.objects.filter(maktab=id)
    if request.method == "POST":
        form = BuyForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.maktab = request.user
            dweet.save()
    return render(request,'crud/buy.html',{'form':form,'buys':buys})

@login_required(login_url='login')
def CreateKitob(request):
    id = request.user
    form = KitobForm()
    books = Kitob.objects.filter(maktab=id)
    if request.method == "POST":
        form = KitobForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.maktab = request.user
            dweet.save()
    return render(request,'crud/Kitob.html',{'form':form,'books':books})
# deletes
@login_required(login_url='login')
def UquvhiDelete(request,id):
    Uquvchi.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('create_uquvchi'))

@login_required(login_url='login')
def SinfDelete(request,id):
    Sinf.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('create_sinf'))

@login_required(login_url='login')
def KitobDelete(request,id):
    Kitob.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('create_kitob'))

@login_required(login_url='login')
def FormularDelete(request,id):
    Buy.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('create_buy'))
# edites
class UquvhciEdit(LoginRequiredMixin,UpdateView):
     model = Uquvchi
     template_name = 'crud/edit.html'
     fields = ['Ismi','Familiya','Sharif','sinf']

class SinfEdit(LoginRequiredMixin,UpdateView):
     model = Sinf
     template_name = 'crud/edit.html'
     fields = ['title','rahbar']

class KitobEdit(LoginRequiredMixin,UpdateView):
     model = Kitob
     template_name = 'crud/edit.html'
     fields = ['title','yosh','description','author','year']

class BuyEdit(LoginRequiredMixin,UpdateView):
     model = Buy
     template_name = 'crud/edit.html'
     fields = ['sender','Kitob','vaqt',]
# export import exel
def Oquvchi_import_excel(request):
    if request.method == 'POST':
        try:
            dataset = Dataset()
            new_p = request.FILES.get('oquvchi')
            print(new_p)

            if not new_p:
                return HttpResponse('Fayl yuklanmadi.')
 
            # Check file format
            if not new_p.name.endswith('.xlsx'):
                return HttpResponse('File formati xato. Faqat .xlsx fayllar qabul qilinadi.')

            imported_data = dataset.load(new_p.read(), format='xlsx')
            for data in imported_data:
                cf = data[3]
                casss = Sinf.objects.get(title=cf)
                value = Uquvchi(
                    Ismi=data[0],
                    Familiya=data[1],
                    Sharif=data[2],
                    sinf=casss,
                    maktab=request.user,
                )
                value.save()

            return HttpResponse('Ma\'lumotlar muvaffaqiyatli yuklandi.')

        except Exception as e:
            return HttpResponse(f'Xatolik yuz berdi: {str(e)}')

    return HttpResponse('Faqat POST so\'rovlari qabul qilinadi.')
     
def Oquvchi_export_exel(request):
    resource = UquvchiRes()
    dataset = resource.export()
    xlsx_format = XLSX()

    response = HttpResponse(content=xlsx_format.export_data(dataset), content_type=xlsx_format.get_content_type())
    response['Content-Disposition'] = 'attachment; filename=uqo`vcilar.xlsx'
    
    return response

def Sinf_import_excel(request):
    if request.method == 'POST':
        try:
            dataset = Dataset()
            new_p = request.FILES.get('sinf')
            print(new_p)

            if not new_p:
                return HttpResponse('Fayl yuklanmadi.')

            # Check file format
            if not new_p.name.endswith('.xlsx'):
                return HttpResponse('File formati xato. Faqat .xlsx fayllar qabul qilinadi.')

            imported_data = dataset.load(new_p.read(), format='xlsx')
            for data in imported_data:
                value = Sinf(
                    title=data[0],
                    rahbar=data[1],
                    maktab=request.user,
                )
                value.save()

            return HttpResponse('Ma\'lumotlar muvaffaqiyatli yuklandi.')

        except Exception as e:
            return HttpResponse(f'Xatolik yuz berdi: {str(e)}')

    return HttpResponse('Faqat POST so\'rovlari qabul qilinadi.')
     
def Sinf_export_exel(request):
    resource = SinfRes()
    dataset = resource.export()
    xlsx_format = XLSX()

    response = HttpResponse(content=xlsx_format.export_data(dataset), content_type=xlsx_format.get_content_type())
    response['Content-Disposition'] = 'attachment; filename=sinflar.xlsx'
    
    return response

def Kitob_import_excel(request):
    if request.method == 'POST':
        try:
            dataset = Dataset()
            new_p = request.FILES.get('kitob')
            print(new_p)

            if not new_p:
                return HttpResponse('Fayl yuklanmadi.')

            # Check file format
            if not new_p.name.endswith('.xlsx'):
                return HttpResponse('File formati xato. Faqat .xlsx fayllar qabul qilinadi.')

            imported_data = dataset.load(new_p.read(), format='xlsx')
            for data in imported_data:
                value = Kitob(
                    title=data[0],
                    yosh=data[1],
                    description=data[2],
                    author=data[3],
                    year=data[4],
                    maktab =request.user,
                )
                value.save()

            return HttpResponse('Ma\'lumotlar muvaffaqiyatli yuklandi.')

        except Exception as e:
            return HttpResponse(f'Xatolik yuz berdi: {str(e)}')

    return HttpResponse('Faqat POST so\'rovlari qabul qilinadi.')
     
def Kitob_export_exel(request):
    resource = KitobRes()
    dataset = resource.export()
    xlsx_format = XLSX()

    response = HttpResponse(content=xlsx_format.export_data(dataset), content_type=xlsx_format.get_content_type())
    response['Content-Disposition'] = 'attachment; filename=Kitoblar.xlsx'
    
    return response

@login_required(login_url='login')
def Dashboard_Tekshiruv(request):
    if request.user.type == 'tekshiruvchi':
        schools = School.objects.all()
        schools_count = School.objects.all().count()
        con = {
            'school':schools,
            'school_count':schools_count,
        }
    return render(request,'tekshiruv/index.html',con)
@login_required(login_url='login')
def Tekshiruvlar(request):
    if request.method == "POST":
        form = KitobForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.maktab = request.user
            dweet.save()
    return render(request,'tekshiruv/tekshiruv.html')



