from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url, re_path
from django.contrib.auth.decorators import login_required
from .views import *
from . import views
from django.conf import settings 
from django.conf.urls.static import static 

app_name = 'userManager'
urlpatterns = [
    path('pmedia/images/<slug:image_name>/',login_required(views.sid), name='SecureImages' ),
    re_path(r'pmedia/$',login_required(views.sid), name='SecureImages' ),
    re_path(r'smedia/$',login_required(views.test_path_trigger), name='TestSecureImages' ),
    path('', index, name='index'),
    path('home/', login_required(home), name='home'),
    path('register/',register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('upload/', login_required(PhotosUploadView.as_view()), name='upload'),
    path('list/', login_required(PhotosListview.as_view()), name='list'),
    path('view/<int:pk>', login_required(PhotosHDView.as_view()), name='details'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                    document_root=settings.MEDIA_ROOT)