from django.db import models


class Receita(models.Model):
    id = models.AutoField('id', primary_key=True)
    descricao = models.CharField(
        'descricao', max_length=255, null=False, blank=False,
        unique_for_month='data'
    )
    valor = models.DecimalField(
        'valor', max_digits=8, decimal_places=2, null=False, blank=False)
    data = models.DateField('data', null=False, blank=False)

    def __str__(self) -> str:
        return self.descricao
