from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("registro/", views.registro_view, name="registro"),
    path("logout/", views.logout_view, name="logout"),

    path("home/", views.home, name="home"),
    path("produccion/", views.produccion, name="produccion"),
    path("envasado/", views.envasado, name="envasado"),
    path("stock/", views.stock, name="stock"),
    path("palets/", views.palets, name="palets"),
    path("despacho/", views.despacho, name="despacho"),
]