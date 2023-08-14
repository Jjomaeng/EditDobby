from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('main/', views.main, name='main'),    
    path('signup/', views.signup, name='signup'),    
    path('login/', views.login, name='login'),    
    path('logout/', views.logout, name='logout'),  
    path('my/', views.my, name='my'),   
    # path('activate/<str:uidb64>/<str:token>', views.Activate.as_view(), name='status'), 
]