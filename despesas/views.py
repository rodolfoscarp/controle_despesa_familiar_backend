from rest_framework import viewsets
from despesas.models import Despesa
from despesas.serializers import DespesaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DespesaFilter(filters.FilterSet):

    descricao = filters.CharFilter(
        field_name="descricao", lookup_expr='contains'
    )

    class Meta:
        model = Despesa
        fields = ('descricao', )


class DespesaViewSet(viewsets.ModelViewSet):
    """ Listagem de despesas """
    queryset = Despesa.objects.all().order_by('-data')
    serializer_class = DespesaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DespesaFilter


class DespesasPorMesView(ListAPIView):
    """ Listagem de despesas por Mes """

    serializer_class = DespesaSerializer

    def get_queryset(self):
        ano = self.kwargs.get('ano')
        mes = self.kwargs.get('mes')

        queryset = Despesa.objects.filter(
            data__year=ano, data__month=mes
        )

        return queryset

    @swagger_auto_schema(operation_id='despesa_mes_list', manual_parameters=[
        openapi.Parameter('ano', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
        openapi.Parameter('mes', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
    ], responses={200: DespesaSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
