from django.urls import path,re_path
from . import views
from django.conf import settings ##新增
from django.views import static ##新增



urlpatterns = [
    re_path('chart(|/)',views.Chart.as_view()),
    re_path('empty(|/)', views.Empty.as_view()),
    re_path('form(|/)', views.Form.as_view()),
    re_path('index(|/)', views.Index.as_view()),
    re_path('tab-panel(|/)', views.Tab_panel.as_view()),
    re_path('table(|/)', views.Table.as_view()),
    re_path('ui-elements(|/)', views.Ui_elements.as_view()),
    path('native', views.Native.as_view()),
    path('host/<int:atkid>/', views.attack, name='host'),
]
