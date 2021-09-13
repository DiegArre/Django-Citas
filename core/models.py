from re import U
from django.db import models
from django.db.models.deletion import CASCADE
from account.models import User
# Create your models here.

class CitaManager(models.Manager):

    def validator(self, postData):
        errors = {}

        #Caracteres Autor
        if len(postData["autor"]) < 4:
            errors["autor"] = "Autor tiene que ser mayor a 3 caracteres"

        #Caracteres Cita
        if len(postData["cita"]) < 11: 
            errors["cita"] = "La Cita tiene que ser mayor a 10 caracteres"

        return errors

class Cita(models.Model):
    autor = models.CharField(max_length=85)
    cita = models.CharField(max_length=280)
    user = models.ForeignKey(User,related_name="citas",on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CitaManager()
    #likes



class Like(models.Model):
    cita = models.ForeignKey(Cita, related_name="likes",on_delete=CASCADE)
    user = models.ForeignKey(User, related_name="my_likes",on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)