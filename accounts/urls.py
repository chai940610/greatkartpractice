from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout,name='logout'),
    path('activate/<girl>/<boy>/',views.activate,name='activate'),
    path('',views.dashboard,name='dashboard'),
    #forgot password
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('resetpassvalid/<salam>/<babi>/',views.resetpassvalid,name='resetpassvalid'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
]
