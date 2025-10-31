from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Usuarios


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['username'].widget.attrs['class'] =  'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña' 
        self.fields['password'].widget.attrs['class'] =  'form-control' 




class FormularioUsuario(forms.ModelForm):
    password1 = forms.CharField(label= 'Contraseña', widget = forms.PasswordInput(
        attrs = { 
        'class': 'form-control',
        'placeholder': 'Ingrese contraseña',
        'id': 'password1',
        'required': 'required',
        }
    ))

    password2 = forms.CharField(label= 'Contraseña de confirmacion', widget = forms.PasswordInput(
        attrs = { 
        'class': 'form-control',
        'placeholder': 'Ingrese nuveamente la contraseña',
        'id': 'password2',
        'required': 'required',
        }
    ))

    class Meta: 
        model = Usuarios
        fields = ('email', 'username', 'nombre', 'apellido')
        widgets = {
            'email': forms.EmailInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder' : 'Correo Electronico',
                }
            ),
            'nombre': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder' : 'Ingrese su nombre',
                }

            ),
            'apellido': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder' : 'Ingrese su apellido',
                }
            ),
            # 'rol': forms.TextInput(
            #     attrs= {
            #         'class': 'form-control',
            #         'placeholder' : 'Ingrese el rol',
            #     }
            # ), 
            'username': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder' : 'Ingrese su nombre de usuario',
                }
            )
        }
    def clean_password2(self):  #validacion de contraseña del form personalizado
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden')
        return password2
    
    def save(self, commit = True):
        user = super().save(commit= False)
        user.set_password(self.cleaned_data['password1'])

        # Asignar rol por defecto si no se definió
        if not user.rol_id:
            from .models import Roles
            rol, _ = Roles.objects.get_or_create(nombre="Administrativo")
            user.rol = rol

        if commit:
            user.save()
        return user

"""   
class UsuarioAutenticacionFormulario(forms.Form):
    username = forms.CharField(max_length=60)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta:
        model = Usuarios
        fields = ("username", "password")
        
    def clean(self):  
        if self.is_valid():
            nombre_usuario = self.cleaned_data['nombre_usuario']  
            password = self.cleaned_data['password']
            if not authenticate(username=nombre_usuario, password=password):
                raise forms.ValidationError("Invalid login")   
    """
    
"""

class LoginForm(forms.Form):
    nombre_usuario = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def clean(self):
        cleaned_data = super().clean()
        nombre_usuario = cleaned_data.get("nombre_usuario")
        password = cleaned_data.get("password")
        
        user = authenticate(nombre_usuario=nombre_usuario, password=password)
        if not user:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user
        
"""