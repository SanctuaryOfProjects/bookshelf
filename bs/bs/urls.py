"""
URL configuration for bs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from onlineplatform.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('my_ads/', my_ads, name='my_ads'),
    path('ad/<int:ad_id>/', ads_detail, name='ad_detail'),
    path('bookcrossing_ads/', bookcrossing_ads, name='bookcrossing_ads'),
    path('add_to_bookshelf/<int:book_id>/', add_to_bookshelf, name='add_to_bookshelf'),
    path('bookshelf/', bookshelf, name='bookshelf'),
    path('cabinet/', cabinet, name='cabinet'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('catalog/', book_list, name='catalog'),
    path('catalog/<int:pk>/', book_detail, name='book_detail'),
    path('register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
