from django.db import models
from django.contrib.auth.models import User

class FalsaPosicion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    funcion = models.CharField(max_length=255, help_text="Ingresa la función en términos de x, por ejemplo: x**3 - x - 2")
    x0 = models.FloatField(help_text="Extremo izquierdo del intervalo")
    x1 = models.FloatField(help_text="Extremo derecho del intervalo")
    tolerancia = models.FloatField(default=0.0001, help_text="Tolerancia del método")
    max_iteraciones = models.IntegerField(default=100, help_text="Número máximo de iteraciones")
    grafico_base64 = models.TextField(blank=True, null=True)
    resultado = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ecuación: {self.funcion} en [{self.x0}, {self.x1}]"
    
    class Meta:
        verbose_name = "Cálculo Falsa Posición"
        verbose_name_plural = "Cálculos Falsa Posición"
        ordering = ['-creado']


class GaussEliminacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    matriz_a = models.TextField(help_text="Matriz A como lista de listas")
    vector_b = models.TextField(help_text="Vector b como lista")
    resultado = models.TextField(blank=True, null=True)
    grafico_base64 = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gauss Eliminación: {self.usuario.username}"

    class Meta:
        verbose_name = "Cálculo Gauss"
        verbose_name_plural = "Cálculos Gauss"
        ordering = ['-creado']


class GaussJordan(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    matriz_a = models.TextField(help_text="Matriz A como lista de listas")
    vector_b = models.TextField(help_text="Vector b como lista")
    resultado = models.TextField(blank=True, null=True)
    grafico_base64 = models.TextField(blank=True, null=True)
    matriz_transformada = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gauss-Jordan: {self.usuario.username}"

    class Meta:
        verbose_name = "Cálculo Gauss-Jordan"
        verbose_name_plural = "Cálculos Gauss-Jordan"
        ordering = ['-creado']
