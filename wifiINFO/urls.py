from django.urls import path,re_path
from . import views
from django.conf import settings ##新增
from django.views import static ##新增



urlpatterns = [
    path('index',views.Index.as_view()),

    re_path(r'^wifi/', views.Mywifi.as_view()),
    re_path(r'^station/',views.Mystation.as_view()),
    path('runoob/', views.runoob),
]
