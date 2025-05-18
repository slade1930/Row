from django.urls import path
from django.views.generic import TemplateView
from .views import (
    FalsaPosicionFormView,
    FalsaPosicionListView,
    EliminarCalculoView,
    FalsaPosicionListCreateView,
    FalsaPosicionDetailView,

    MetodoSeleccionView,

    GaussEliminacionListView,
    GaussEliminacionFormView,
    EliminarGaussEliminacionView,
    GaussEliminacionListCreateView,
    GaussEliminacionDetailView,

    GaussJordanListView,
    GaussJordanFormView,
    EliminarGaussJordanView,
    GaussJordanListCreateView,
    GaussJordanDetailView,
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='metodo/inicio.html'), name='inicio'),

    # Falsa Posición
    path("falsa-posicion/", FalsaPosicionListView.as_view(), name="list_falsa_posicion"),
    path("falsa-posicion/agregar/", FalsaPosicionFormView.as_view(), name="add_falsa_posicion"),
    path("falsa-posicion/eliminar/<int:id>/", EliminarCalculoView.as_view(), name="eliminar_calculo"),
    path("api/falsa-posicion/", FalsaPosicionListCreateView.as_view(), name="api_falsa_posicion_list_create"),
    path("api/falsa-posicion/<int:pk>/", FalsaPosicionDetailView.as_view(), name="api_falsa_posicion_detail"),

    # Vista de selección de métodos
    path("metodo/", MetodoSeleccionView.as_view(), name="metodo_seleccion"),

    # Gauss Eliminación
    path("gauss-eliminacion/", GaussEliminacionListView.as_view(), name="list_gauss_eliminacion"),
    path("gauss-eliminacion/agregar/", GaussEliminacionFormView.as_view(), name="add_gauss_eliminacion"),
    path("gauss-eliminacion/eliminar/<int:id>/", EliminarGaussEliminacionView.as_view(), name="eliminar_gauss_eliminacion"),
    path("api/gauss-eliminacion/", GaussEliminacionListCreateView.as_view(), name="api_gauss_eliminacion_list_create"),
    path("api/gauss-eliminacion/<int:pk>/", GaussEliminacionDetailView.as_view(), name="api_gauss_eliminacion_detail"),

    # Gauss-Jordan
    path("gauss-jordan/", GaussJordanListView.as_view(), name="list_gauss_jordan"),
    path("gauss-jordan/agregar/", GaussJordanFormView.as_view(), name="add_gauss_jordan"),
    path("gauss-jordan/eliminar/<int:id>/", EliminarGaussJordanView.as_view(), name="eliminar_gauss_jordan"),
    path("api/gauss-jordan/", GaussJordanListCreateView.as_view(), name="api_gauss_jordan_list_create"),
    path("api/gauss-jordan/<int:pk>/", GaussJordanDetailView.as_view(), name="api_gauss_jordan_detail"),
]
