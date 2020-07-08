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
    # path('protected/', login_required(views.secure_image_delivery), name='403Error_1'),
	# path('media/', login_required(views.media_folder_only), name='403Error_1'),
	# path('media/images/', login_required(views.media_folder_only), name='403Error_2'),
	# path('media/images/<slug:image_id>/', login_required(views.secure_image_delivery), name='SecureImages'),
	re_path(r'^media/$',login_required(views.sid), name='SecureImages' ),

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