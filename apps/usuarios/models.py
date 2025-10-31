from django.contrib.auth.models import BaseUserManager,  AbstractBaseUser
from django.db import models

class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class UsuariosManager(BaseUserManager):
    def create_user(self, email, username, nombre, apellido, rol=None,  password=None):
        if not email:
            raise ValueError("Usuario tiene que tener un email")
        
        # Si no se pasa un rol, asignar uno por defecto
        if rol is None:
            rol, creado = Roles.objects.get_or_create(nombre="Administrativo")  # Rol por defecto

        usuario = self.model(
            username = username,
            email=self.normalize_email(email),
            nombre=nombre, 
            apellido=apellido,
            rol=rol, 
            
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario
    
    
    
    def create_superuser(self, username, email, nombre, apellido, password, rol=None):

        if rol is None:
            rol, _ = Roles.objects.get_or_create(nombre="Admin")

        usuario = self.create_user(
            email = email,
            username= username,
            nombre = nombre,
            apellido = apellido,
            rol = rol,
            password=password,
        )

        
        usuario.is_admin = True
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)
        return usuario




class Usuarios(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique= True, max_length=60)
    email = models.EmailField('Correo electronico', max_length=254, unique= True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    #rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    # rol = models.CharField(max_length=20)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    is_admin = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
   

    objects = UsuariosManager()
     
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email'] #campos necesarios para crear la cuenta por consola

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"

    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

"""
class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nombre_usuario = models.CharField(max_length=60)
    password = models.CharField(max_length=255)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.nombre_usuario})"
"""