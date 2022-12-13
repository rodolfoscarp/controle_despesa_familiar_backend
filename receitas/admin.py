from django.contrib import admin
from receitas.models import Receita


class ReceitaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Receita, ReceitaAdmin)
