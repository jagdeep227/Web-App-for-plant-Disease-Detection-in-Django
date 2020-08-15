from django.conf.urls import url
from . import views

from django.contrib.auth import views as auth_views
from django.urls import path


app_name = 'farming'

urlpatterns=[

    url(r'^$' , views.home , name='home'),
    url(r'^display_info$' , views.display_info , name='display_info'),
    url(r'^register$' , views.register , name='register'),

    path('login/', auth_views.LoginView.as_view(), name='login1'),
    url(r'^check_new$' , views.check_new , name='check_new'),
    url(r'^del_pics$' , views.delete_pics , name='delete_pics'),
    url(r'^check_new2$' , views.check_new2 , name='check_new2'),
    url(r'^check_old$' , views.check_old , name='check_old'),
    url(r'^logout$' , views.logout_view , name='logout_view'),
]