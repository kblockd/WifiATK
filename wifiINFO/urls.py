from django.urls import path,re_path
from . import views
from django.conf import settings ##新增
from django.views import static ##新增
from django.views.generic import RedirectView


urlpatterns = [

    path('chart/',views.Chart.as_view()),
    path('empty/', views.Empty.as_view()),
    path('form/', views.Form.as_view()),
    path('tab-panel/', views.Tab_panel.as_view()),
    path('ui-elements/', views.Ui_elements.as_view()),

    re_path(r'^$', RedirectView.as_view(url='index/')),
    path('index/', views.Index.as_view()),
    path('active/', views.Active.as_view()),
    path('wifilog/',views.Wifi.as_view()),
    path('stationlog/',views.Station.as_view()),

    path('host/start/<int:wifi_id>/', views.host_atk, name='host'),
    path('host/stop/<int:wifi_id>/', views.host_atk, name='host'),

]
