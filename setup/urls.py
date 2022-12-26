from django.contrib import admin
from django.urls import path, include
from receitas.views import ReceitaViewSet, ReceitaPorMesView
from despesas.views import DespesaViewSet, DespesasPorMesView
from resumo.views import ResumoPorMesView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'receitas', ReceitaViewSet)
router.register(r'despesas', DespesaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path(r'receitas/<int:ano>/<int:mes>',
         ReceitaPorMesView.as_view(), name='receita_mes'),
    path(r'despesas/<int:ano>/<int:mes>',
         DespesasPorMesView.as_view(), name='despesa_mes'),
    path(r'resumo/<int:ano>/<int:mes>',
         ResumoPorMesView.as_view(), name='resumo_mes')
]
