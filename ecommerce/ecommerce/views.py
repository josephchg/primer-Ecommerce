from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ContactForm, LoginForm, RegisterForm


#metodo de vista con su contexto
def home_page(request):
    context={
        "title":"Hola mundo",
        "content":"Bienvenidos a la pagina",
    }
    #si el usuario se autentico, en la pag de inicio mostrara un mensaje
    if request.user.is_authenticated():
        context['premiun_content']="yeahhhhh"
    return render(request,'home_page.html',context)

def about_page(request):
    context={
        "title":"Pagina de acerca de",
        "content":"Bienvenidoa a pagina acerca de"
    }
    return render(request,'home_page.html',context)
#metodo usando forms com un metodo post
def contact_page(request):
    #se importo la clase de forms
    contact_form=ContactForm(request.POST or None)
    context={
        "title":"Contacto",
        "content":"Bienvenidos a pagina de contacto",
        "form":contact_form
    }
    if contact_form.is_valid():
        #muestra los datos ingresados en la terminal si se registro correctamente
        print(contact_form.cleaned_data)

        #forma tradicional
        #if request.method=="POST":
        #print(request.POST)
        #print(request.POST.get("name"))
        #print(request.POST.get("email"))
        #print(request.POST.get("content"))"""
    return render(request,'contact/view.html',context)

#funcion para logearse si tienes superusuario
def login_page(request):
    form=LoginForm(request.POST or None)
    context = {
        'form': form
    }
    print("Logeando")
    #print(request.user.is_authenticated())
    #si se escribio los campos correctos
    if form.is_valid():
        print(form.cleaned_data)
        #obtenemos lso campos de formulario login
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        #nos da un booleano si es usuario correcto o no
        user = authenticate(request, username=username, password=password)
        #print(request.user.is_authenticated())
        #si el usuario no es vacio
        if user is not None:
            #nos logeamos
            login(request, user)
            # Redirect to a success page.
            return redirect('/')
        else:
            # Return an 'invalid login' error message.
            print("Error")
    return render(request,'auth/login.html',context)

#se importo para usar el modelo de user
User=get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        #obtenemos los datos que se pasaron
        username=form.cleaned_data.get('username')
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')
        #creamos un usuario de acuerdo a los 3 parametros
        new_user=User.objects.create_user(username,email,password)
        return redirect('/login')
    return render(request,'auth/register.html',context)

