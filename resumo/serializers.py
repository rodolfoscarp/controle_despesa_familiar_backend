from rest_framework import serializers


class TotalCategoriaDespesaSerializer(serializers.Serializer):

    categoria = serializers.CharField()
    total = serializers.FloatField()

    class Meta:
        fields = ['categoria', 'total']


class ResumoSerializer(serializers.Serializer):

    total_receitas = serializers.FloatField()
    total_despesas = serializers.FloatField()
    saldo = serializers.FloatField()
    categorias_despesas = TotalCategoriaDespesaSerializer(many=True)

    class Meta:
        fields = ['total_receitas', 'total_despesas',
                  'saldo', 'categorias_despesas']
