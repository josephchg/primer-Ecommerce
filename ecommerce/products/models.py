import os
from django.db import models
import random
#para usar el slug ramdon es necesario importar esto y crear un archivo utils.py
from django.db.models.signals import pre_save,post_save
from .utils import unique_slug_generator
#para el uso de reverse
from django.urls import reverse

#metodo para obtener el nombre y extension de manera separada
def get_filename_ext(filepath):
    #obtener el nombre del archivo completo con su extension
    base_name=os.path.basename(filepath)
    #obtener el nombre y la extension
    name,ext=os.path.splitext(base_name)
    return name,ext

#metodo para tener varias carpetas con las imagen media
def upload_image_path(instance,filename):
    new_filename=random.randint(1,3910209312)
    #llamamos al metodo para separar
    name,ext=get_filename_ext(filename)
    final_filename='{name}{ext}'.format(name=name,ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

#para combinar las consultas mediante funciones en otras clases
class ProductQuerySet(models.query.QuerySet):
    #funcion activo producto
    def active(self):
        return self.filter(active=True)
    #funcion featured
    def featured(self):
        return self.filter(featured=True,active=True)

#para hacer consultas mediante manager de modelos
class ProductManager(models.Manager):
    #para poder usar las funciones de consultas de la class ProductQueryset
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    #combinar con la funcion active
    def all(self):
        return self.get_queryset().active()

    #funcion con la funcion featured
    def featured(self):
        return self.get_queryset().featured()

    #metodo para obtener el id y verificar si existe
    def get_by_id(self,id):
        qs=self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        return None

#se crea los modelos, es decir las tablas con sus campos de nuestra bd
class Product(models.Model):
    title       = models.CharField(max_length=120)
    #para poner url de acuerdo al titulo
    slug        = models.SlugField(blank=True,unique=True)
    description = models.TextField()
    price       = models.DecimalField(max_digits=20,decimal_places=2,default=39.99)
    image       = models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    #sirve para poner el models.manager la funcion featured y asi filtrar de acuerdo al valor bool
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    #hereda de la clase de manager de modelos
    objects     = ProductManager()
    #para obtener el tiempo
    timestamp   = models.DateTimeField(auto_now_add=True)

    #metodo para redireccionar un producto con su detalle
    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        #manera correcta de redireccionar con reverse mediante el namespace y name
        return reverse('products:detail',kwargs={"slug":self.slug})

    def __str__(self):
        return self.title

#permite obtener un slug de acuerod al title, y si ya existiera le aumenta algo
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

#guardar la informacion en el clase Prduct
pre_save.connect(product_pre_save_receiver,sender=Product)