from rest_framework.test import APITestCase
from django.urls import reverse
from despesas.models import Despesa
from receitas.models import Receita
from datetime import date
from decimal import Decimal


class ResumoTest(APITestCase):

    def cadastrar_nova_receita(
            self, descricao=None, valor=None,
            data=None
    ):

        receita = Receita(
            descricao=descricao or "Receita Teste",
            valor=valor or Decimal('100'),
            data=data or date(2022, 1, 1),
        )

        receita.save()

    def cadastrar_nova_despesa(
        self, descricao=None, valor=None,
        data=None, categoria=None
    ):

        despesa = Despesa(
            descricao=descricao or "Despesa Teste",
            valor=valor or Decimal('100'),
            data=data or date(2022, 1, 1),
            categoria=categoria or 'Outros'
        )
        despesa.save()

    def test_deve_detalhar_resumo_por_mes(self):

        data = date(2022, 1, 1)

        self.cadastrar_nova_despesa(
            data=data, descricao="Despesa1", valor=Decimal('100'), categoria='Outros'
        )
        self.cadastrar_nova_despesa(
            data=data, descricao="Despesa2", valor=Decimal('20'), categoria='Saúde'
        )
        self.cadastrar_nova_despesa(
            data=data, descricao="Despesa3", valor=Decimal('30'), categoria='Outros'
        )

        self.cadastrar_nova_receita(
            data=data, descricao="Receita1", valor=Decimal('150'))
        self.cadastrar_nova_receita(
            data=data, descricao="Receita2", valor=Decimal('50'))
        self.cadastrar_nova_receita(
            data=data, descricao="Receita3", valor=Decimal('20'))

        res = self.client.get(
            reverse('resumo_mes', kwargs={'ano': 2022, 'mes': 1}))

        response_data = res.json()

        self.assertEqual(
            response_data['total_receitas'], 220
        )
        self.assertEqual(
            response_data['total_despesas'], 150
        )
        self.assertEqual(
            response_data['saldo'], 70
        )

        self.assertEqual(
            response_data['categorias_despesas'], [
                {'categoria': 'Outros', 'total': 130.0},
                {'categoria': 'Saúde', 'total': 20.0}
            ]
        )
