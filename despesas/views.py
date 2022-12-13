from rest_framework import viewsets
from despesas.models import Despesa
from despesas.serializers import DespesaSerializer


class DespesaViewSet(viewsets.ModelViewSet):
    queryset = Despesa.objects.all().order_by('-data')
    serializer_class = DespesaSerializer
