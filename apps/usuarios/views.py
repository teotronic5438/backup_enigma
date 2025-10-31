from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
#from django.utils.decorators import method_decorator
#from django.views.decorators.cache import never_cache
#from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FormularioLogin, FormularioUsuario
from django.contrib.auth import login as auth_login, authenticate, logout
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Usuarios, Roles


class LogoutUsuarioView(LoginRequiredMixin, LogoutView):
    next_page = '/usuarios/login/'
    
# def logoutUsuario(request):
#      logout(request)
#      return HttpResponseRedirect('/usuarios/login/')  #ex: return HttpResponseRedirect('usuarios:login')

class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = FormularioLogin
    redirect_authenticated_user = True
    next_page = reverse_lazy('core:dashboard')

    def get_context_data(self, **kwargs):
        """Añade la variable 'is_login_page' al contexto de la plantilla."""
        context = super().get_context_data(**kwargs)
        context['is_login_page'] = True
        return context

    def get_success_url(self):
        return self.get_redirect_url() or self.next_page

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('core:dashboard')  

#     if request.method == 'POST':
#         form = FormularioLogin(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)
#             return redirect('core:dashboard')
#     else:
#         form = FormularioLogin()

#     return render(request, 'usuarios/login.html', {'form': form})

    
class RegistrarUsuario(CreateView):
      model = Usuarios
      form_class = FormularioUsuario
      template_name = 'usuarios/register.html'
      success_url = reverse_lazy('core:dashboard')
      
      def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
                  # Asignar un rol por defecto (ej: "Usuario")
                  rol, _ = Roles.objects.get_or_create(nombre="Administrativo")
                  nuevo_usuario = Usuarios(
                        email = form.cleaned_data.get('email'),
                        username = form.cleaned_data.get('username'), 
                        nombre = form.cleaned_data.get('nombre'),
                        apellido = form.cleaned_data.get('apellido'),
                        rol = rol
                  )
                  nuevo_usuario.set_password(form.cleaned_data.get('password1'))
                  nuevo_usuario.save()
                  messages.success(request, '¡Registro exitoso! Ya puede iniciar sesion.')
                  return redirect('usuarios:login')
            else:
                  return render(request, self.template_name, {'form': form})
      
# """

# class Login(LoginView):
#     template_name = 'usuarios/login.html'  #otra opcion de cargar el loginview
#     authentication_form = FormularioLogin
#     redirect_authenticated_user = True #hace un redirect a LOGIN_REDIRECT_URL de settings.py
# """


# """"
# def logoutUsuario(request):
#      logout(request)
#      return HttpResponseRedirect('/login/')  
# """



# """"" Intentos fallidos 

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('core:home')  # Cambia a la url que uses para el home

#     if request.method == 'POST':
#         form = FormularioLogin(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)
#             return redirect('core:home')
#     else:
#         form = FormularioLogin()

#     return render(request, 'usuarios/login.html', {'form': form})


# class Login(FormView):
#     template_name = 'usuarios/login.html'
#     form_class = FormularioLogin
#     success_url = reverse_lazy('core:home')
      
#     @method_decorator(csrf_protect)
#     @method_decorator(never_cache)
#     def dispatch(self, request, *args, **kwargs): 
#         print(request.user)
#         if request.user.is_authenticated:
#             print("INGRESO AL IF DE REQUESR,USER.ISAUTHENTICA") #bORRAR ESTO DESPS DE PROBAR 
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             print("NO INGRESO") #bORRAR ESTO DESPS DE PROBAR 
#             return super(Login,self).dispatch(request, *args, **kwargs)
    
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         print("User to login:", user)
#         return super(Login,self).form_valid(form)
#  """     

      

         

# """"


# def register_view(request, *args, **kwargs):
#     #user = request.user 
#     #if user.is_authenticated:
#      #   return HttpResponse(f"Ya esta autenticado como {user.nombre_usuario}") --> la validacion la hace el form directamente. )
#     context = {}
    
#     if request.method == "POST":
#         form = UsuarioFormulario(request.POST)
#         if form.is_valid():
#             usuario = form.save(commit=False)
#             usuario.username = usuario.nombre_usuario
#             usuario.save()
            
#             nombre_usuario = form.cleaned_data.get('nombre_usuario')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(request, username = nombre_usuario, password = raw_password)
#             login(request, user)
#             print("paso por el if ")
#             return redirect("core:Home")
#         else: 
#             context['registration_form'] = form
#     else:
#         form = UsuarioFormulario()
#         context['registration_form'] = form
             

#     return render (request, 'usuarios/register.html', context)
 
# def logout_view(request):
#     logout(request)
#     return redirect("core:Home")           

# def login_view(request, *args, **kwargs):
# 	context = {}
# 	#user = request.user
# 	#if user.is_authenticated: 
# #		return redirect("core:Home")

# 	if request.method == "POST":
# 		form = UsuarioAutenticacionFormulario(request.POST)
# 		if form.is_valid():
# 			nombre_usuario = form.cleaned_data.get('nombre_usuario')
# 			password = form.cleaned_data.get('password')
# 			user = authenticate(request, username = nombre_usuario, password=password)
#             #nombre_usuario = request.POST['nombre_usuario']
# 			#password = request.POST['password']
# 			#usuario = authenticate(username = nombre_usuario, password=password)
# 			if user is not None:
# 				login(request, user)
# 				return redirect("core: home")
    
# 	else:
# 		form = UsuarioAutenticacionFormulario()

# 	context['login_form'] = form

# 	return render(request, "usuarios/login.html", context)           
                            

# """
# """

# def registro_view(request):
#     if request.method == 'POST':
#         form = UsuarioFormulario(data=request.POST)
#         if form.is_valid():
#             usuario = form.save()
#             login(request, usuario)
#             return redirect('core:Home')  # o a donde quieras redirigir después del registro
#     else:      
          
#         form = UsuarioFormulario()
#     return render(request, 'registracion.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('core:Home')
#         else:
#             messages.error(request, "Usuario o contraseña incorrectos")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# def login_view(request):
#     form = LoginForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect('core:Home')  # o donde quieras ir
#     return render(request, 'usuarios/login.html', {'form': form})
#     """