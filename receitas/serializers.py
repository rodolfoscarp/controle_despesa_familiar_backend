from rest_framework import serializers
from receitas.models import Receita


class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ['id', 'descricao', 'valor', 'data']
