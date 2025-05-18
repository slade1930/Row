from django.contrib import admin
from .models import FalsaPosicion


class FalsaPosicionAdmin(admin.ModelAdmin):
    model = FalsaPosicion
    list_display = ["funcion", "x0", "x1", "tolerancia", "max_iteraciones", "creado"]
    search_fields = ["funcion"]
    list_filter = ["creado"]
    readonly_fields = ["resultado", "creado"]
    fieldsets = (
        (None, {
            'fields': ('funcion', 'x0', 'x1', 'tolerancia', 'max_iteraciones')
        }),
        ('Resultados', {
            'fields': ('resultado', 'creado'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(FalsaPosicion, FalsaPosicionAdmin)