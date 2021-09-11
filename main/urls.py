from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('travels/add', views.new_trip),
    path('travels_delete/<id_p>',views.delete_plan),
    path('view/<id_p>', views.show_details),
    path('join_plan/<id_p>', views.join_trip)
]
