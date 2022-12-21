from rest_framework import serializers
from despesas.models import Despesa


class DespesaSerializer(serializers.ModelSerializer):

    valor = serializers.FloatField()
    data = serializers.DateField()

    class Meta:
        model = Despesa
        fields = ['id', 'descricao', 'valor', 'data', 'categoria']
