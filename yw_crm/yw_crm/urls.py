"""yw_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from stark.service.stark import site
from crm import views

urlpatterns = [
    path('verify_code/', views.verify_code),
    path('admin/', admin.site.urls),
    path('stark/',site.urls),
    path('rbac/', include('rbac.urls',namespace='rbac')),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('index/', views.IndexView.as_view(), name='index'),

    path('reset/', views.ResetView.as_view(), name='reset'),
    # path('reset/', views.reset,name='reset'),

    path('test/', views.test),

]
