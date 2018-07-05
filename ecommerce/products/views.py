from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Product

#vista basada en clase para mostrar todos los objetos con funcion featured
class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    #metodos para obtener todos los objetos mediante queryset
    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.all().featured()

#vista basada en clase para mostrar detalle individual de cada objeto con funcion featured
class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"

    #metodo con queryset para filtrar por id
    #def get_queryset(self,*args,**kwargs):
    #    request=self.request
    #    return Product.objects.featured()

#vista basada en clase para mostrar todos los objetos
class ProductListView(ListView):
    #consulta para obtener todos los objetos de mi tabla product
    queryset = Product.objects.all()
    #a que plantilla ira
    template_name = "products/list.html"
    #funciona como contexto
    #def get_context_data(self,*args,**kwargs):
    #    context=super(ProductListView,self).get_context_data(*args,**kwargs)
    #   return context

    #metodos para obtener todos los objetos mediante queryset
    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.all()

#vista basada en funcion para mostrar todos los objetos
def product_list_view(request):
    queryset = Product.objects.all()
    context ={
        'object_list':queryset
    }
    return render(request,"products/list.html",context)

#vista de clase para usar el slug en las url
class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_object(self, *args,**kwargs):
        request=self.request
        slug=self.kwargs.get('slug')
        #manejador de errores
        try:
            instance=Product.objects.get(slug=slug,active=True)
        #si el producto no existe
        except Product.DoesNotExist:
            raise Http404("No existe")
        #si el producto tienen el mismo slug
        except Product.MultipleObjectsReturned:
            qs= Product.objects.filter(slug=slug,active=True)
            instance=qs.first()
        except:
            raise Http404("Ahhh")
        return instance

#vista basada en clase para mostrar detalle individual de cada objeto
class ProductDetailView(DetailView):
    #consulta para obtener todos los objetos de mi tabla product
    #queryset = Product.objects.all()
    #a que plantilla ira
    template_name = "products/detail.html"
    #funciona como contexto
    def get_context_data(self,*args,**kwargs):
        context=super(ProductDetailView,self).get_context_data(*args,**kwargs)
        #context['abc']=123
        return context

    #metodo para mostrar un error si no hay el producto, busqueda por id
    def get_object(self,*args,**kwargs):
        request=self.request
        pk=self.kwargs.get('pk')
        instance=Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Producto no existe")
        return instance

    #metodo con queryset para filtrar por id
    #def get_queryset(self,*args,**kwargs):
    #    request=self.request
    #    pk=self.kwargs.get('pk')
    #    return Product.objects.filter(pk=pk)

#vista basada en funcion para mostrar detalle individual de cada objeto
def product_detail_view(request,pk=None,*args,**kwargs):
    #instance = Product.objects.get(pk=pk)
    #si existe un objecto que no encuentra por su pk bota ese error
    #instance = get_object_or_404(Product,pk=pk)

    #manejador de error si un pk no existe
    #try:
    #    instance=Product.objects.filter(id=pk)
    #except Product.DoesNotExist:
    #    print("no producto aqui")
    #    raise Http404("Producto no existe")

    #usa la funcion de manager de modelos para obtener una instancia
    instance=Product.objects.get_by_id(pk)
    #si no se encontro
    if instance is None:
        raise Http404("Producto no existe")
    #consulta base a un filtro por id
    #qs=Product.objects.filter(id=pk)
    #si el id existe y realiza una consulta
    #if qs.exists() and qs.count()==1:
        #una mejor manera de get
       # instance=qs.first()
    #else:
    #   raise Http404("Producto no existe")
    context ={
       'object':instance
    }
    return render(request,"products/detail.html",context)