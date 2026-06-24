from django.db import models


TIPO_CHOICES = [
    ('60', '60'),
    ('68', '68'),
    ('120', '120'),
    ("CRISTIx60", "CRISTIx60"),
]

CATEGORIA_CHOICES = [
    ('buena', 'Buena'),
    ('mala', 'Mala'),
    ('especial', 'Especial'),
]


class Produccion(models.Model):
    nombre_operario = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    buenas = models.IntegerField(default=0)
    malas = models.IntegerField(default=0)
    especiales = models.IntegerField(default=0)

    fecha = models.DateField()

    def total(self):
        return self.buenas + self.malas + self.especiales
    
class Envasado(models.Model):
    nombre_operario = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    cantidad = models.IntegerField()
    fecha = models.DateField()


class MovimientoStock(models.Model):
    usuario = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)


class Palet(models.Model):
    tipo = models.CharField(max_length=50)
    lote = models.CharField(max_length=20)
    cajas = models.IntegerField(default=0)

    class Meta:
        unique_together = ('tipo', 'lote')


class Despacho(models.Model):
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    lote = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

class Stock(models.Model):
    nombre_operario = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    buenas = models.IntegerField(default=0)
    malas = models.IntegerField(default=0)
    especiales = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre_operario} - {self.tipo}"