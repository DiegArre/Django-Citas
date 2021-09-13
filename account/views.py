from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User
import bcrypt
# Create your views here.


def logout(request): 
    if "usuario" in request.session:
        del request.session["usuario"]
        messages.info(request,"Vuelve pronto!")
    return redirect("/account/login")

def login(request):
    if request.method == "GET":
        if "usuario" in request.session:
            messages.info(request,"Ya estas logueado!!")
            return redirect("/")
        return render(request,"account/login.html")


    if request.method == "POST":
        usuario = User.objects.filter(email = request.POST["email"].lower())
        if usuario:
            logged_user = usuario[0]
        else:
            messages.warning(request,"El email no se encuentra registrado!")
            return redirect("/account/login")

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):

            request.session["usuario"] = {
                "id" : logged_user.id,
                "nombre" : logged_user.nombre,
                "apellido" : logged_user.apellido,
                "email" : logged_user.email,
            }
            messages.success(request,"Logueado correctamente")
            return redirect("/")
        else:
            messages.error(request,"Contraseña incorrecta!")
        return redirect("/account/login")


def register(request):
    if request.method == "GET":
        if "usuario" in request.session:
            messages.info(request,"Para registrar una cuenta debes salir de la actual!")
            return redirect("/")
        else:
            return render(request,"account/register.html")


    if request.method == "POST":
        print(request.POST)

        usuario = User.objects.filter(email = request.POST["email"].lower())
        if usuario:
            messages.warning(request, "Este email ya se encuentra registrado")
            return redirect("/account/register")

        errors = User.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0 :
            
            for key, value in errors.items():

                messages.error(request,value)

            return redirect("/account/register")   

        else:
            new_user = User.objects.create(
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                email = request.POST["email"].lower(),
                password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            )
            print("SE HA CREADO LA CUENTA")
            messages.success(request, "Te has registrado correctamente!")
            return redirect("/account/login")
        

def edit(request):
    if request.method == "GET":
        if "usuario" in request.session:
            return render(request,"account/edit_user.html")
        else:
            messages.info(request,"Debes estar logueado para editar tus datos")
            return redirect("/account/login")

    if request.method == "POST":

        #validacion cambio de datos

        if request.session["usuario"]["nombre"] == request.POST["nombre"] and request.session["usuario"]["apellido"] == request.POST["apellido"] and request.session["usuario"]["email"] == request.POST["email"].lower():
            messages.info(request, "Los datos enviado deben ser diferentes a los actuales!")
            return redirect("/account/edit")
        ###email en la base de datos
        if request.session["usuario"]["email"] != request.POST["email"]:
            usuario = User.objects.filter(email = request.POST["email"].lower())
            if usuario:
                messages.warning(request, "Este email ya se encuentra registrado, intenta con otro")
                return redirect("/account/edit")
        #validacion regex modelos
        errors = User.objects.edit_validator(request.POST)
        print(errors)
        if len(errors) > 0 :

            for key, value in errors.items():
                messages.error(request,value)
            return redirect("/account/edit")   

        #Actualizando
        
        user_u = User.objects.get(id = request.session["usuario"]["id"])
        user_u.nombre = request.POST["nombre"]
        user_u.apellido = request.POST["apellido"]
        user_u.email = request.POST["email"]
        user_u.save()
        request.session["usuario"]["nombre"] = request.POST["nombre"]
        request.session["usuario"]["apellido"] = request.POST["apellido"]
        request.session["usuario"]["email"] = request.POST["email"]
        request.session.save()

        messages.success(request, "Se han actualizado los datos correctamente!")
        return redirect("/account/edit")

