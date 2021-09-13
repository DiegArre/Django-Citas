import re
from django.shortcuts import redirect, render
from django.contrib import messages
from core.models import Cita, Like, User
# Create your views here.


def index(request):
    if "usuario" in request.session:

        context = {
            "citas" : Cita.objects.all().order_by("-created_at")
        }
        return render(request,"core/citas.html",context)
    else: 
        messages.info(request,"Logueate para continuar!")
        return redirect("/account/login")


def post_cita(request):
    if request.method == "POST":
        print(request.POST)
        errors = Cita.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0 :
            
            for key, value in errors.items():

                messages.error(request,value)

            return redirect("/")  
        
        user_c = User.objects.get(id = request.session["usuario"]["id"])
        cita_c = Cita.objects.create(
            autor = request.POST["autor"],
            cita = request.POST["cita"],
            user = user_c
        )
        messages.success(request,"Se ha añadido la cita correctamente")
        return redirect("/")



def delete_cita(request):
    if request.method == "POST":
        cita_d = Cita.objects.get(id= request.POST["cita_id"])
        cita_d.delete()
        messages.error(request,"La cita se ha eliminado!")
        return redirect("/")


def like_cita(request):
    if request.method == "POST":
        

        cita_l = Cita.objects.get(id = request.POST["cita_id"])
        user_id = request.session["usuario"]["id"]
        user_l = User.objects.get(id = user_id)

        ## Validacion no dar doble like
        likes = cita_l.likes.all()
        print(likes)
        for like in likes:
            if like.user.id == user_id:
                messages.warning(request,"No puedes dar like a la misma publicacion 2 veces :C")
                return redirect("/")

        #Se crea el like
        like = Like.objects.create(
            cita = cita_l,
            user = user_l
        )
        messages.info(request,f"Diste un like al apublicacion de {cita_l.user.nombre} {cita_l.user.apellido}")
        return redirect("/")


def show_user(request,user_id):
    user = User.objects.get(id = user_id )
    context = {
        "user_name" : f"{user.nombre} {user.apellido}",
        "citas" : user.citas.all()
    }

    return render(request,"core/user.html",context)



def start(request):
    return redirect("/account/login")