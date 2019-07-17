from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from game.forms import PlayerRegistrationForm
from registration.backends.simple.views import RegistrationView


urlpatterns = [
    url(r'^', include('game.urls')),

    url(r'^login/$', auth_views.login, {
        'template_name': 'registration/login.html',
        'redirect_authenticated_user': True,
    }, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {
        'template_name': 'registration/logout.html',
    }, name='auth_logout'),
    url(r'^register/$', RegistrationView.as_view(form_class=PlayerRegistrationForm), name='registration_register'),

    url(r'^admin/', admin.site.urls),
]
