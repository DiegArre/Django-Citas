from django.urls import path 
from . import  views

urlpatterns = [
    path("",views.index),
    path("cita/delete",views.delete_cita),
    path("cita/post",views.post_cita),
    path("cita/like",views.like_cita),
    path("user/<int:user_id>",views.show_user)
]