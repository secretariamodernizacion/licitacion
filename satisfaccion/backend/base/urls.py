from rest_framework import routers
from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from base.api import instituciones
from base import views

router = routers.SimpleRouter()

router.register(r'instituciones', instituciones.View,)


urlpatterns = [

    path('data_grafica/', views.data_grafica),
    path('data_grafica/<int:pk>', views.data_grafica),
    path('data_dimension/', views.data_dimension),
    path('data_dimension/<int:pk>', views.data_dimension),
    path('data_imagen/', views.data_imagen),
    path('data_imagen/<int:pk>', views.data_imagen),
    path('data_atributos/', views.data_atributos),
    path('data_atributos/<int:pk>', views.data_atributos),
    path('canal_evaluacion/', views.canal_evaluacion),
    path('canal_evaluacion/<int:pk>', views.canal_evaluacion),
    path('canal_preferencia/', views.canal_preferencia),
    path('canal_preferencia/<int:pk>', views.canal_preferencia),
    path('informe/<str:codigo_dipres>', views.informe),

    path('resumen/', views.resumen)
]


urlpatterns += router.urls
