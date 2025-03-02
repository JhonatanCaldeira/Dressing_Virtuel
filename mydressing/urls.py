"""
URL configuration for mydressing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from photos.views import (
    upload_photos,
    create_user,
    login_view,
    logout_view,
    main_view,
    upload_faceid,
    show_images_from_user,
    edit_image_product,
    delete_multiple_clothes,
    get_suggestion
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #Admin route
    path('admin/', admin.site.urls),

    #Authentication routes
    path('create_user/', create_user, name="create_user"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),

    #Main and user management routes
    path('', main_view, name='index'),
    path('main/', main_view, name="main_view"),
    path('upload_faceid/', upload_faceid, name="upload_faceid"),
    path('upload_photos/', upload_photos, name="upload_photos"),
    path('list_of_clothes/', show_images_from_user, name="list_of_clothes"),
    path('suggestion/', get_suggestion, name="suggestion"),
    path('delete_multiple_clothes/', delete_multiple_clothes, name='delete_multiple_clothes'), 

    #Image product management
    path('edit_image_product/<int:image_product_id>/', edit_image_product, 
         name='edit_image_product'),
    path('', include('django_prometheus.urls'), name='metrics'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)