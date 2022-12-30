from rest_framework import viewsets
from receitas.models import Receita
from receitas.serializers import ReceitaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ReceitaFilter(filters.FilterSet):

    descricao = filters.CharFilter(
        field_name="descricao", lookup_expr='contains'
    )

    class Meta:
        model = Receita
        fields = ('descricao', )


class ReceitaViewSet(viewsets.ModelViewSet):
    """ Listagem de Receitas """
    queryset = Receita.objects.all().order_by('-data')
    serializer_class = ReceitaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReceitaFilter


class ReceitaPorMesView(ListAPIView):
    """ Listagem de receitas por Mes """

    serializer_class = ReceitaSerializer

    def get_queryset(self):
        ano = self.kwargs.get('ano')
        mes = self.kwargs.get('mes')

        queryset = Receita.objects.filter(
            data__year=ano, data__month=mes
        )

        return queryset

    @swagger_auto_schema(operation_id='receitas_mes_list', manual_parameters=[
        openapi.Parameter('ano', openapi.IN_PATH, type=openapi.TYPE_INTEGER),
        openapi.Parameter('mes', openapi.IN_PATH, type=openapi.TYPE_INTEGER)
    ], responses={200: ReceitaSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
