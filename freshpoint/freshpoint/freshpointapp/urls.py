from django.conf.urls import include, url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    # url(r'^$', views.intro, name='intro'),
    url(r'^index.html/$', views.index, name='index'),
    url(r'^upload.html/$', views.upload, name='upload'),
    url(r'^$', auth_views.login, {'template_name': 'freshpointapp/login.html'}, name='login'),
    url(r'^success/$', views.success, name='success'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
]

urlpatterns += staticfiles_urlpatterns()
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
