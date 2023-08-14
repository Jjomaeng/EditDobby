from django.urls import path
from . import views

app_name = 'dobby'

urlpatterns = [
    path('edit/', views.edit, name='edit'),      
    path('result/', views.result, name='result'),
    path('result_thumb/', views.result_thumb, name='result_thumb'), 
    path('title_select/', views.title_select, name='title_select'),     
    path('fun/', views.fun, name='fun'),
    path('result/download/', views.download, name='dobbydown'),
    # path('')    
]