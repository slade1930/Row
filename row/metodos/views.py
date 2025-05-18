from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.generic import CreateView, ListView, View, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FalsaPosicion, GaussEliminacion, GaussJordan
from .serializers import FalsaPosicionSerializer, GaussEliminacionSerializer, GaussJordanSerializer
from .forms import FalsaPosicionForm, GaussEliminacionForm, GaussJordanForm
from .utils import falsa_posicion, generar_grafica, eliminacion_gauss, gauss_jordan, grafica_comparacion_solucion, grafica_matriz_transformada
from users.models import UserProfile
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
import json

# ------------------------- VISTAS PARA FALSA POSICIÓN (EXISTENTES) -------------------------

class FalsaPosicionListView(LoginRequiredMixin, ListView):
    model = FalsaPosicion
    template_name = "metodo/list.html"
    context_object_name = "resultados"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return FalsaPosicion.objects.filter(usuario=self.request.user)
        return FalsaPosicion.objects.none()

class FalsaPosicionFormView(CreateView):
    model = FalsaPosicion
    form_class = FalsaPosicionForm
    template_name = "metodo/add.html"
    success_url = reverse_lazy("list_falsa_posicion")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            calculation_count = self.request.session.get('calculation_count', 0)
            context['calculation_percentage'] = min((calculation_count / 3) * 100, 100)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            calculation_count = request.session.get('calculation_count', 0)
            if calculation_count >= 3:
                messages.error(request, 'Has alcanzado el límite de 3 cálculos. Por favor regístrate para continuar.')
                return redirect('register')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        
        if self.request.user.is_authenticated:
            instance.usuario = self.request.user
            profile, created = UserProfile.objects.get_or_create(user=self.request.user)
            profile.calculations_count = FalsaPosicion.objects.filter(usuario=self.request.user).count()
            profile.save()
        else:
            instance.usuario = None
            self.request.session['calculation_count'] = self.request.session.get('calculation_count', 0) + 1
            self.request.session.modified = True

        resultado, pasos = falsa_posicion(
            funcion=instance.funcion,
            x0=instance.x0,
            x1=instance.x1,
            tol=instance.tolerancia,
            max_iter=instance.max_iteraciones
        )
        instance.resultado = pasos

        if resultado is not None:
            grafico = generar_grafica(instance.funcion, instance.x0, instance.x1, resultado)
            instance.grafico_base64 = grafico

        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        if not self.request.user.is_authenticated:
            messages.info(self.request, 'Regístrate para guardar tu historial de cálculos permanentemente.')
        return super().get_success_url()

@method_decorator(require_POST, name='dispatch')
class EliminarCalculoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            calculo_id = kwargs.get('id')
            calculo = FalsaPosicion.objects.get(id=calculo_id, usuario=request.user)
            calculo.delete()
            
            profile = UserProfile.objects.get(user=request.user)
            profile.calculations_count = FalsaPosicion.objects.filter(usuario=request.user).count()
            profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Cálculo eliminado correctamente'
            })
        except FalsaPosicion.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'El cálculo no existe o no tienes permiso para eliminarlo'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

# ------------------------- VISTAS PARA MÉTODOS DE GAUSS (NUEVAS) -------------------------

class MetodoSeleccionView(TemplateView):
    template_name = "metodo/metodo_seleccion.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['falsa_posicion_form'] = FalsaPosicionForm()
        context['gauss_eliminacion_form'] = GaussEliminacionForm()
        context['gauss_jordan_form'] = GaussJordanForm()
        return context

class GaussEliminacionListView(LoginRequiredMixin, ListView):
    model = GaussEliminacion
    template_name = "metodo/list_gauss.html"
    context_object_name = "resultados"

    def get_queryset(self):
        return GaussEliminacion.objects.filter(usuario=self.request.user)

class GaussEliminacionFormView(LoginRequiredMixin, CreateView):
    model = GaussEliminacion
    form_class = GaussEliminacionForm
    template_name = "metodo/add_gauss.html"
    success_url = reverse_lazy("list_gauss_eliminacion")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.usuario = self.request.user
        
        try:
            matriz_a = json.loads(instance.matriz_a)
            vector_b = json.loads(instance.vector_b)
            
            solucion, pasos = eliminacion_gauss(matriz_a, vector_b)
            
            if solucion is not None:
                instance.resultado = json.dumps({
                    'solucion': solucion,
                    'pasos': pasos
                })
                
                grafico = grafica_comparacion_solucion(matriz_a, vector_b, solucion)
                if grafico:
                    instance.grafico_base64 = grafico
                
                instance.save()
                
                profile = UserProfile.objects.get(user=self.request.user)
                profile.systems_count = GaussEliminacion.objects.filter(usuario=self.request.user).count()
                profile.save()
                
                return super().form_valid(form)
            else:
                messages.error(self.request, "Error en el cálculo: " + pasos)
                return self.form_invalid(form)
                
        except json.JSONDecodeError:
            messages.error(self.request, "Formato incorrecto en matriz o vector")
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f"Error: {str(e)}")
            return self.form_invalid(form)

class GaussJordanListView(LoginRequiredMixin, ListView):
    model = GaussJordan
    template_name = "metodo/list_gauss_jordan.html"
    context_object_name = "resultados"

    def get_queryset(self):
        return GaussJordan.objects.filter(usuario=self.request.user)

class GaussJordanFormView(LoginRequiredMixin, CreateView):
    model = GaussJordan
    form_class = GaussJordanForm
    template_name = "metodo/add_gauss_jordan.html"
    success_url = reverse_lazy("list_gauss_jordan")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.usuario = self.request.user
        
        try:
            matriz_a = json.loads(instance.matriz_a)
            vector_b = json.loads(instance.vector_b)
            
            solucion, pasos, matriz_transformada = gauss_jordan(matriz_a, vector_b)
            
            if solucion is not None:
                instance.resultado = json.dumps({
                    'solucion': solucion,
                    'pasos': pasos
                })
                
                if matriz_transformada is not None:
                    grafico = grafica_matriz_transformada(matriz_transformada)
                    if grafico:
                        instance.grafico_base64 = grafico
                        instance.matriz_transformada = json.dumps(matriz_transformada.tolist())
                
                instance.save()
                
                profile = UserProfile.objects.get(user=self.request.user)
                profile.systems_count = GaussJordan.objects.filter(usuario=self.request.user).count()
                profile.save()
                
                return super().form_valid(form)
            else:
                messages.error(self.request, "Error en el cálculo: " + pasos)
                return self.form_invalid(form)
                
        except json.JSONDecodeError:
            messages.error(self.request, "Formato incorrecto en matriz o vector")
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f"Error: {str(e)}")
            return self.form_invalid(form)

@method_decorator(require_POST, name='dispatch')
class EliminarGaussEliminacionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            calculo_id = kwargs.get('id')
            calculo = GaussEliminacion.objects.get(id=calculo_id, usuario=request.user)
            calculo.delete()
            
            profile = UserProfile.objects.get(user=request.user)
            profile.systems_count = GaussEliminacion.objects.filter(usuario=request.user).count()
            profile.save()
            
            return JsonResponse({'success': True, 'message': 'Cálculo eliminado correctamente'})
        except GaussEliminacion.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El cálculo no existe o no tienes permiso'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@method_decorator(require_POST, name='dispatch')
class EliminarGaussJordanView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            calculo_id = kwargs.get('id')
            calculo = GaussJordan.objects.get(id=calculo_id, usuario=request.user)
            calculo.delete()
            
            profile = UserProfile.objects.get(user=request.user)
            profile.systems_count = GaussJordan.objects.filter(usuario=request.user).count()
            profile.save()
            
            return JsonResponse({'success': True, 'message': 'Cálculo eliminado correctamente'})
        except GaussJordan.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El cálculo no existe o no tienes permiso'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

# ------------------------- API VIEWS (ACTUALIZADAS) -------------------------

class FalsaPosicionListCreateView(ListCreateAPIView):
    queryset = FalsaPosicion.objects.all()
    serializer_class = FalsaPosicionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        profile.calculations_count = FalsaPosicion.objects.filter(usuario=self.request.user).count()
        profile.save()

class FalsaPosicionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = FalsaPosicion.objects.all()
    serializer_class = FalsaPosicionSerializer
    permission_classes = [IsAuthenticated]

class GaussEliminacionListCreateView(ListCreateAPIView):
    queryset = GaussEliminacion.objects.all()
    serializer_class = GaussEliminacionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        profile.systems_count = GaussEliminacion.objects.filter(usuario=self.request.user).count()
        profile.save()

class GaussEliminacionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = GaussEliminacion.objects.all()
    serializer_class = GaussEliminacionSerializer
    permission_classes = [IsAuthenticated]

class GaussJordanListCreateView(ListCreateAPIView):
    queryset = GaussJordan.objects.all()
    serializer_class = GaussJordanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        profile.systems_count = GaussJordan.objects.filter(usuario=self.request.user).count()
        profile.save()

class GaussJordanDetailView(RetrieveUpdateDestroyAPIView):
    queryset = GaussJordan.objects.all()
    serializer_class = GaussJordanSerializer
    permission_classes = [IsAuthenticated]