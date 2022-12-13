from rest_framework import viewsets
from receitas.models import Receita
from receitas.serializers import ReceitaSerializer


class ReceitaViewSet(viewsets.ModelViewSet):
    """ Receitas """
    queryset = Receita.objects.all().order_by('-data')
    serializer_class = ReceitaSerializer
