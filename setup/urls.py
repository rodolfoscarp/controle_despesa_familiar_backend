from django.contrib import admin
from django.urls import path, include
from receitas.views import ReceitaViewSet
from despesas.views import DespesaViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'receitas', ReceitaViewSet)
router.register(r'despesas', DespesaViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
