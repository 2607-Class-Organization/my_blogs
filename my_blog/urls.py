"""
URL configuration for my_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth import views as auth_view
from two_factor.urls import urlpatterns as two_factor_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogs.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include((two_factor_urlpatterns[0], 'two_factor'), namespace='two_factor')),
    path('school/', include('school.urls')),
    path('accounts/register', RegistrationView.as_view(success_url='registration_complete'), name='django_registration'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
]

handler404 = 'blogs.views.error_404_view'
