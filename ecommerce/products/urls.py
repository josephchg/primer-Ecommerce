from django.conf.urls import url

from .views import (
    ProductListView,
    ProductDetailSlugView
    )

urlpatterns = [
    #se enlaza con las urls principales
    url(r'^$', ProductListView.as_view(),name='list'),
    #darle un name para asi poder usar reverse
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(),name='detail'),
]

