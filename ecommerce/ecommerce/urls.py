"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url,include

from django.conf import settings
from django.conf.urls.static import static
#importar boostrap mediante un html creado en la carpeta template
from django.views.generic import TemplateView

#from products.views import (
#    product_list_view,
#    ProductListView,
#    ProductDetailView,
#    product_detail_view,
#    ProductFeaturedListView,
#    ProductFeaturedDetailView,
#    ProductDetailSlugView,
#    )

from .views import home_page, about_page, contact_page, login_page, register_page

urlpatterns = [
    #poner las url para acceder a la views,poner de argumento name para asi permitir redireccionar
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page,name='home'),
    url(r'^about/$', about_page,name='about'),
    url(r'^contact/$', contact_page,name='contact'),
    url(r'^login/$', login_page,name='login'),
    url(r'^register/$', register_page,name='register'),
    #poner el boostrap en funcionamiento, redirecciona de acuerdo al template_name
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
    #nos permite dirigirnos a las urls de un app mediante include,ademas poner un namespace
    url(r'^products/', include("products.urls",namespace='products')),
    #vista basada en clase
    #url(r'^products/$', ProductListView.as_view()),
    #vista basada en funcion
    #url(r'^products-fbv/$', product_list_view),
    #expresiones regulares para detallar cada producto
    #url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
    #url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
    #vista de lista y detalle con funcion featured
    #url(r'^featured/$', ProductFeaturedListView.as_view()),
    #url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
    #vista para usar el slug
    #url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
]
#para poner tanto archivos y medias estaticos listos para la produccion
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
