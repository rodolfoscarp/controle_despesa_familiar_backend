from django.db import models


class Despesa(models.Model):

    class CategoriaDespesa(models.TextChoices):
        ALIMENTACAO = 'Alimentação'
        SAUDE = 'Saúde'
        MORADIA = 'Moradia'
        TRANSPORTE = 'Transporte'
        EDUCACAO = 'Educação'
        LAZER = 'Lazer'
        IMPREVISTOS = 'Imprevistos'
        OUTRAS = 'Outras'

    id = models.AutoField('id', primary_key=True)
    descricao = models.CharField(
        'descricao', max_length=255, null=False, blank=False,
        unique_for_month='data'
    )
    valor = models.DecimalField(
        'valor', max_digits=8, decimal_places=2, null=False, blank=False)
    data = models.DateField('data', null=False, blank=False)
    categoria = models.CharField(
        max_length=15, null=False, blank=False, default=CategoriaDespesa.OUTRAS,
        choices=CategoriaDespesa.choices
    )

    def __str__(self) -> str:
        return self.descricao
