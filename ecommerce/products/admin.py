from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Product
#poner nuestros modelos en el admin

#clase para administrar en el admin el modelo
class ProductAdmin(admin.ModelAdmin):
    #campos a visualizar
    list_display = ['__str__','slug']
    #subclase para definir el modelo
    class Meta:
        model=Product

admin.site.register(Product,ProductAdmin)