from rest_framework import serializers
from despesas.models import Despesa


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = ['id', 'descricao', 'valor', 'data']
