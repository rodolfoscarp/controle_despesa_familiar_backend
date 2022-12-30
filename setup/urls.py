from django.contrib import admin
from django.urls import path, include, re_path
from receitas.views import ReceitaViewSet, ReceitaPorMesView
from despesas.views import DespesaViewSet, DespesasPorMesView
from resumo.views import ResumoPorMesView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = routers.DefaultRouter()
router.register(r'receitas', ReceitaViewSet)
router.register(r'despesas', DespesaViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Controle de Despesa Familiar API",
        default_version='v1',
        description="Controle de Despesa Familiar",
        contact=openapi.Contact(email="rodolfoscarp@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path(r'receitas/<int:ano>/<int:mes>',
         ReceitaPorMesView.as_view(), name='receita_mes'),
    path(r'despesas/<int:ano>/<int:mes>',
         DespesasPorMesView.as_view(), name='despesa_mes'),
    path(r'resumo/<int:ano>/<int:mes>',
         ResumoPorMesView.as_view(), name='resumo_mes'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'
            ),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
