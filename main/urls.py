from django.urls import path
from .views import *
urlpatterns = [
    path('',Home,name='home'),
    path('maktab/',Dashboard_Maktab,name='maktab'),
    path("maktab/formulay/finish/<int:id>/",finish_formuliyar, name="f_F"),
    # ko`rish
    path('maktab/formulyar/',Formulayrs,name='formulars'),
    path('maktab/formulyar/topshirilgan/',Topshirilgan,name='topshirilgan'),
    path('maktab/formulyar/topshirilmagan/',Topshirilmagan,name='topshirilmagan'),
    path('maktab/kitoblar/',Kitoblar,name='kitob'),
    # create
    path('maktab/crud/oquvchi',CreateUquvchi,name='create_uquvchi'),
    path('maktab/crud/sinf',CreateSinf,name='create_sinf'),
    path('maktab/crud/buys',CreateBuy,name='create_buys'),
    path('maktab/crud/books',CreateKitob,name='create_books'),
    # edit
    path('maktab/crud/edit1/<int:pk>/',UquvhciEdit.as_view(),name='edit_uquvchi'),
    path('maktab/crud/edit2/<int:pk>/',SinfEdit.as_view(),name='edit_sinf'),
    path('maktab/crud/edit3/<int:pk>/',KitobEdit.as_view(),name='edit_kitob'),
    path('maktab/crud/edit4/<int:pk>/',BuyEdit.as_view(),name='edit_buy'),
    # delete
    path('maktab/crud/delete1/<int:id>/',UquvhiDelete,name='delete_uquvchi'),
    path('maktab/crud/delete2/<int:id>/',SinfDelete,name='delete_sinf'),
    path('maktab/crud/delete3/<int:id>/',KitobDelete,name='delete_kitob'),
    path('maktab/crud/delete4/<int:id>/',SinfDelete,name='delete_buy'),
    # tekshiruv
    path('tekshiruv/',Dashboard_Tekshiruv,name='tekshiruv'),
    # import_export
    path('exel/import/file/oquvchi/',Oquvchi_import_excel,name='oquchi_import'),
    path('exel/export/file/oquvchi/',Oquvchi_export_exel,name='oquchi_export'),

    path('exel/import/file/sinf/',Sinf_import_excel,name='sinf_import'),
    path('exel/export/file/sinf/',Sinf_export_exel,name='sinf_export'),

    path('exel/import/file/kitob/',Kitob_import_excel,name='kitob_import'),
    path('exel/export/file/kitob/',Kitob_export_exel,name='kitob_export'),
]
