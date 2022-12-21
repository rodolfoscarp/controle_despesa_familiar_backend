from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Sum
from resumo.serializers import TotalCategoriaDespesaSerializer
from despesas.models import Despesa
from receitas.models import Receita


class ResumoPorMesView(ListAPIView):

    def list(self, request, *args, **kwargs):

        ano = kwargs['ano']
        mes = kwargs['mes']

        despesas = Despesa.objects.filter(data__year=ano, data__month=mes)
        receitas = Receita.objects.filter(data__year=ano, data__month=mes)

        total_despesas = despesas.aggregate(
            total_despesas=Sum('valor')).get('total_despesas') or 0

        total_receitas = receitas.aggregate(
            total_receitas=Sum('valor')).get('total_receitas') or 0

        saldo = total_receitas - total_despesas

        total_categorias_despesas = despesas.values('categoria').annotate(
            total=Sum('valor')
        )

        categorias_despesas = TotalCategoriaDespesaSerializer(
            total_categorias_despesas, many=True).data

        return Response(
            {
                'total_receitas': total_receitas,
                'total_despesas': total_despesas,
                'saldo': saldo,
                'categorias_despesas': categorias_despesas
            }
        )
