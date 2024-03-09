"""
URL configuration for vote_system project.

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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Default path to admin panel:
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    # Connect all our paths from app - MAIN from file urls.py in this app:
    path('', include('main.urls')),


    # WITH using INCLUDE function we make our main app more independent(независимым) from vote_system project.
]

# Когда мы работаем в режиме отладки, нам нужно сэмулировать работу реального рабочего/боевого веб сервера для
# получения ранее загруженных файлов и передачи их нашему приложению
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)