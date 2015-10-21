from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'signin$', views.sign_in, name='sign_in'),
    url(r'signedin$', views.signed_in, name='signed_in'),
    url(r'notebooks$', views.notebooks, name='notebooks'),
    url(r'sections$', views.sections, name='sections'),
    url(r'pages$', views.pages, name='pages'),
    url(r'page$', views.page, name='page'),
]