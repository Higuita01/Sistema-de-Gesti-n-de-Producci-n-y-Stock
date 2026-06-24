from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.utils.timezone import now
from django.db import models
from .models import Produccion, Stock
from django.contrib import messages
from .models import Produccion
from django.contrib import messages
from .models import Stock, Envasado
from django.contrib import messages
from datetime import datetime,date

from .models import Produccion, MovimientoStock, Palet, Despacho


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "login.html")


def registro_view(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        return redirect("login")
    return render(request, "registro.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    return render(request, "home.html")


# ---------------- PRODUCCIÓN ----------------

@login_required
def produccion(request):

    if request.method == "POST":

        nombre = request.POST.get("nombre").strip()
        tipo = request.POST.get("tipo").strip()

        buenas = int(request.POST.get("buenas") or 0)
        malas = int(request.POST.get("malas") or 0)
        especiales = int(request.POST.get("especiales") or 0)

        # 1️⃣ Guardar registro histórico
        fecha_str = request.POST.get("fecha")
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

        Produccion.objects.create(
          nombre_operario=nombre,
          tipo=tipo,
          buenas=buenas,
          malas=malas,
          especiales=especiales,
          fecha=fecha
        )

        # 2️⃣ Crear o actualizar stock
        stock, created = Stock.objects.get_or_create(
            nombre_operario=nombre,
            tipo=tipo,
            defaults={
                "buenas": 0,
                "malas": 0,
                "especiales": 0
            }
        )

        stock.buenas += buenas
        stock.malas += malas
        stock.especiales += especiales

        stock.save()

        return redirect("produccion")

    datos = Produccion.objects.order_by("-fecha")
    return render(request, "produccion.html", {"datos": datos})


# ---------------- ENVASADO ----------------

from datetime import datetime, date

@login_required
def envasado(request):

    if request.method == "POST":

        nombre = request.POST.get("nombre").strip()
        tipo = request.POST.get("tipo").strip()
        categoria = request.POST.get("categoria").strip()
        cantidad = int(request.POST.get("cantidad") or 0)

        fecha_str = request.POST.get("fecha")
        if fecha_str:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        else:
            fecha = date.today()

        stock = Stock.objects.filter(
            nombre_operario__iexact=nombre,
            tipo=tipo
        ).first()

        if not stock:
            messages.error(request, "No existe stock para ese operario y tipo.")
            return redirect("envasado")

        if categoria == "buena":
            if cantidad > stock.buenas:
                messages.error(request, "No hay suficientes buenas en stock.")
                return redirect("envasado")
            stock.buenas -= cantidad

        elif categoria == "mala":
            if cantidad > stock.malas:
                messages.error(request, "No hay suficientes malas en stock.")
                return redirect("envasado")
            stock.malas -= cantidad

        elif categoria == "especial":
            if cantidad > stock.especiales:
                messages.error(request, "No hay suficientes especiales en stock.")
                return redirect("envasado")
            stock.especiales -= cantidad

        stock.save()

         # 🔥 SI QUEDA TODO EN 0, SE ELIMINA EL REGISTRO
        if stock.buenas == 0 and stock.malas == 0 and stock.especiales == 0:
           stock.delete()

        Envasado.objects.create(
            nombre_operario=nombre,
            tipo=tipo,
            categoria=categoria,
            cantidad=cantidad,
            fecha=fecha
        )

        return redirect("envasado")

    datos = Envasado.objects.order_by("-fecha")
    return render(request, "envasado.html", {"datos": datos})

# ---------------- STOCK ----------------

@login_required
def stock(request):

    stock_operario = Stock.objects.all().order_by("nombre_operario", "tipo")

    totales = (
        Stock.objects
        .values("tipo")
        .annotate(
            total_buenas=Sum("buenas"),
            total_malas=Sum("malas"),
            total_especiales=Sum("especiales"),
        )
        .order_by("tipo")
    )

    return render(request, "stock.html", {
        "stock_operario": stock_operario,
        "totales": totales
    })


# ---------------- PALETS ----------------

@login_required
def palets(request):

    mensaje = ""

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        lote = request.POST.get("lote")

        palet, created = Palet.objects.get_or_create(
            tipo=tipo,
            lote=lote,
            defaults={
                "cajas": 0,
            }
        )

        if not created:
            palet.cajas += 1
        else:
            palet.cajas = 1

        palet.save()

        mensaje = "✅ Palet agregado correctamente"

        return redirect("palets")

    # Esto se ejecuta cuando abres la página (GET)
    lista = Palet.objects.all().order_by("-id")

    return render(request, "palets.html", {
        "lista": lista,
        "mensaje": mensaje,
    })

# ---------------- DESPACHO ----------------

@login_required
def despacho(request):

    mensaje = ""

    if request.method == "POST":

        tipo = request.POST.get("tipo")
        lote = request.POST.get("lote")
        cantidad = int(request.POST.get("cantidad") or 0)

        try:
            palet = Palet.objects.get(lote=lote, tipo=tipo)

            if cantidad <= 0:
                mensaje = "❌ Cantidad inválida"

            elif cantidad > palet.cajas:
                mensaje = "❌ No hay suficientes palets"

            else:
                palet.cajas -= cantidad

                # 🔥 SI QUEDA EN 0, SE BORRA COMPLETAMENTE
                if palet.cajas == 0:
                    palet.delete()
                else:
                    palet.save()

                mensaje = "✅ Despacho realizado correctamente"

        except Palet.DoesNotExist:
            mensaje = "❌ No existe ese lote para ese tipo"

        return redirect("despacho")

    return render(request, "despacho.html", {
        "mensaje": mensaje
    })
