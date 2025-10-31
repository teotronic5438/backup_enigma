from django.urls import path, include
#from django.contrib.auth.decorators import login_required
from .views import  LogoutUsuarioView, UsuarioLoginView, RegistrarUsuario#, login_view
# from .views import  logoutUsuario,  RegistrarUsuario, login_view #, Login


app_name = 'usuarios'
urlpatterns = [
 
    path('register/',  RegistrarUsuario.as_view(), name ='register'),
    #path('login/',  login_view, name ='login'), 
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    # path('logout/',  login_required(logoutUsuario) , name ='logout'),
    

]