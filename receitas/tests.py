from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from receitas.models import Receita
from datetime import date
from decimal import Decimal

url = reverse('receita-list')


class ReceitaViewSetTest(APITestCase):

    def cadastrar_nova_receita(self):

        receita = Receita(
            descricao="Receita Teste",
            valor=Decimal('100'),
            data=date(2022, 1, 1)
        )

        receita.save()

    def test_deve_cadastrar_nova_receita(self):
        receita = dict(
            descricao="Receita Teste",
            valor=Decimal('100'),
            data=date(2022, 1, 1)
        )

        res = self.client.post(url, receita, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(receita['descricao'], Receita.objects.get().descricao)
        self.assertAlmostEqual(
            Decimal(receita['valor']), Receita.objects.get().valor)
        self.assertEqual(receita['data'], Receita.objects.get().data)

    def test_nao_deve_cadastrar_duas_receitas_com_mesma_descricao_dentro_do_mesmo_mes(self):
        receita_1 = dict(
            descricao="Receita Teste",
            valor=Decimal('100'),
            data=date(2022, 1, 1)
        )

        receita_2 = receita_1.copy()
        receita_2['data'] = date(2022, 1, 2)

        self.client.post(url, receita_1, format='json')

        res = self.client.post(url, receita_2, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deve_listar_receitas_cadastradas(self):
        self.cadastrar_nova_receita()

        res = self.client.get(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

    def test_deve_atualizar_uma_receita(self):
        self.cadastrar_nova_receita()
        receita = Receita.objects.get()

        data = dict(
            descricao="Receita Teste Atualizada",
            valor=Decimal('150'),
            data=date(2022, 1, 10)
        )

        pk = receita.pk

        res = self.client.put(f'{url}{pk}/', data=data, format='json')

        receita_atualizada = Receita.objects.get()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(receita_atualizada.descricao, data['descricao'])
        self.assertAlmostEqual(receita_atualizada.valor, data['valor'])
        self.assertEqual(receita_atualizada.data, data['data'])

    def test_deve_deletar_um_receita(self):
        self.cadastrar_nova_receita()
        receita = Receita.objects.get()

        pk = receita.pk

        res = self.client.delete(f'{url}{pk}/', format='json')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
