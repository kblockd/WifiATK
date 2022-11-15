from django.urls import path, re_path
from . import views
# from django.conf import settings ##新增
# from django.views import static ##新增
from django.views.generic import RedirectView


urlpatterns = [

    re_path(r'^$', RedirectView.as_view(url='index/')),
    path('index/', views.UI),
    path('api/index/', views.Index_api.as_view(), name='index'),
    path('api/active/', views.Active_api.as_view(), name='active'),
    path('api/wifi/', views.Wifi_api.as_view(), name='wifi'),
    path('api/station/', views.Station_api.as_view(), name='station'),

    path('api/attack/start/<wifi_bssid>/', views.attack, name='attack_start'),
    path('api/attack/stop/<wifi_bssid>/', views.attack, name='attack_stop'),

    path('api/config/get/', views.Config_api.as_view(), name='config_get'),
    path('api/config/set/<key>/<value>', views.Config_api.set, name='config_set'),

    # path('activelog/',views.Active_api.as_view()),
    # path('host/start/<int:wifi_id>/', views.host_atk, name='host'),
    # path('host/stop/<int:wifi_id>/', views.host_atk, name='host'),

]
