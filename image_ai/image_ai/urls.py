"""image_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from login import views
from .settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
# from django.views import static
# from django.conf import settings
# from django.conf.urls import url


urlpatterns = [
    # path('admin/', admin.site.urls),

    # use custom administration system
    path('admin/login/', views.admin_login),

    # users' interface
    path('login/', views.login),
    path('logon/', views.logon),
    path('logout/', views.logout),
    path('index/', views.index),
    path('about/', views.about),
    path('record/<username>/', views.record, name='record'),
	# url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media')

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
