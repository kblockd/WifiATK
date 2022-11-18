from django.urls import path, re_path
from . import views
# from django.conf import settings ##新增
# from django.views import static ##新增
from django.views.generic import RedirectView


urlpatterns = [

    re_path(r'^$', RedirectView.as_view(url='index/')),
    path('index/', views.webui),
    path('api/index/', views.Indexapi.as_view(), name='index'),
    path('api/active/', views.Activeapi.as_view(), name='active'),
    path('api/wifi/', views.Wifiapi.as_view(), name='wifi'),
    path('api/station/', views.Stationapi.as_view(), name='station'),

    path('api/attack/start/<str:wifi_bssid>/', views.attack, name='attack_start'),
    path('api/attack/stop/<str:wifi_bssid>/', views.attack, name='attack_stop'),

    path('api/config/get/', views.Configapi.as_view(), name='config_get'),
    path('api/config/set/<str:key>/<str:value>/', views.Configapi.set, name='config_set'),

    # path('activelog/',views.Active_api.as_view()),
    # path('host/start/<int:wifi_id>/', views.host_atk, name='host'),
    # path('host/stop/<int:wifi_id>/', views.host_atk, name='host'),

]
