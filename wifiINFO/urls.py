from django.urls import path,re_path
from . import views
from django.conf import settings ##新增
from django.views import static ##新增



urlpatterns = [
    path('chart',views.Chart.as_view()),
    path('empty', views.Empty.as_view()),
    path('form', views.Form.as_view()),
    path('index', views.Index.as_view()),
    path('tab-panel', views.Tab_panel.as_view()),
    path('table', views.Table.as_view()),
    path('ui-elements', views.Ui_elements.as_view()),
    path('attack/<int:atkid>/', views.attack, name='attack'),
]
