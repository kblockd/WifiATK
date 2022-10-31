from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^wifi/', views.Mywifi.as_view()),
    re_path(r'^station/',views.Mystation.as_view()),
    path('runoob/', views.runoob),
]
