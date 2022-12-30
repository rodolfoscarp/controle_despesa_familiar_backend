from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from resumo.serializers import TotalCategoriaDespesaSerializer, ResumoSerializer
from despesas.models import Despesa
from receitas.models import Receita
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ResumoPorMesView(APIView):

    @swagger_auto_schema(operation_id='resumo_mes_list', manual_parameters=[
        openapi.Parameter('ano', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
        openapi.Parameter('mes', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
    ], responses={200: ResumoSerializer})
    def get(self, request, *args, **kwargs) -> dict:

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
