from despesas.models import Despesa
from rest_framework import serializers


class TotalCategoriaDespesaSerializer(serializers.Serializer):

    categoria = serializers.CharField()
    total = serializers.FloatField()

    class Meta:
        fields = ['categoria', 'total']
