from rest_framework import serializers
from .models import FalsaPosicion, GaussEliminacion, GaussJordan

class FalsaPosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FalsaPosicion
        fields = '__all__'

class GaussEliminacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaussEliminacion
        fields = '__all__'

class GaussJordanSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaussJordan
        fields = '__all__'
