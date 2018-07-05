from django import forms
from django.contrib.auth import get_user_model

#para usar el modelo de usuario y asi registrar
User=get_user_model()

#se creo la clase para un formulario con su widget que permita modifica la estructura
class ContactForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput(
                                attrs={
                                    "class":"form-control",
                                    "placeholder":"Nombre completo"
                                }
                        ))
    email=forms.EmailField(widget=forms.EmailInput(
                                attrs={
                                    "class":"form-control",
                                    "placeholder":"Correo"
                                }
                        ))
    content=forms.CharField(widget=forms.Textarea(
                                attrs={
                                    "class": "form-control",
                                    "placeholder": "Contenido"
                                }
                                ))
    #funcion para validar correo
    def clean_email(self):
        #obtiene el valor del campo email
        email=self.cleaned_data.get("email")
        #si esa expresion no esta contenido en email,dara error
        if not "gmail.com" in email:
            raise forms.ValidationError("Correo necesita @gmail.com")
        return email

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username=forms.CharField()
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirmar password",widget=forms.PasswordInput)

    #para verificar si existe un usuario ya creado
    def clean_username(self):
        username=self.cleaned_data.get('username')
        #realizamos un filtro al objeto usuario mediante su useranme
        qs= User.objects.filter(username=username)
        #si existe ya un usuario manda un  mensaje de error
        if qs.exists():
            raise forms.ValidationError('Existe un usuario ya creado con ese nombre')
        return username

    #lo mismo de arriba pero para email
    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs= User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Ya tiene una cuenta con ese correo')
        return email

    #para validar que las contraseñas que se ingresaron sean iguales
    def clean(self):
        data=self.cleaned_data
        password=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Contraseñas incorrectas")
        return data