from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from despesas.models import Despesa
from datetime import date
from decimal import Decimal

url = reverse('despesa-list')


class DespesaTest(APITestCase):

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

    def test_deve_cadastrar_nova_despesa(self):
        despesa = dict(
            descricao="Despesa Teste",
            valor=Decimal('100'),
            data=date(2022, 1, 1),
            categoria='Alimentação'
        )

        res = self.client.post(url, despesa, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(despesa['descricao'], Despesa.objects.get().descricao)
        self.assertAlmostEqual(
            Decimal(despesa['valor']), Despesa.objects.get().valor)
        self.assertEqual(despesa['data'], Despesa.objects.get().data)
        self.assertEqual(despesa['categoria'], Despesa.objects.get().categoria)

    def test_nao_deve_cadastrar_despesas_com_categoria_invalida(self):
        despesa = dict(
            descricao="Despesa Teste",
            valor=Decimal('100'),
            data=date(2022, 1, 1),
            categoria='Outra Descrição'
        )

        res = self.client.post(url, despesa, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deve_atribuir_categoria_outras_ao_cadastrar_nova_despesa_se_categoria_nao_for_informada(self):
        despesa = dict(
            descricao="Despesa Teste",
            valor=Decimal('100'),
            data=date(2022, 1, 1),
        )

        res = self.client.post(url, despesa, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(despesa['descricao'], Despesa.objects.get().descricao)
        self.assertAlmostEqual(
            Decimal(despesa['valor']), Despesa.objects.get().valor)
        self.assertEqual(despesa['data'], Despesa.objects.get().data)
        self.assertEqual("Outras", Despesa.objects.get().categoria)

    def test_nao_deve_cadastrar_duas_despesas_com_mesma_descricao_dentro_do_mesmo_mes(self):
        despesa_1 = dict(
            descricao="Despesa Teste",
            valor=Decimal('100'),
            data=date(2022, 1, 1)
        )

        despesa_2 = despesa_1.copy()
        despesa_2['data'] = date(2022, 1, 2)

        self.client.post(url, despesa_1, format='json')

        res = self.client.post(url, despesa_2, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deve_listar_despesas_cadastradas(self):
        self.cadastrar_nova_despesa()

        res = self.client.get(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

    def test_deve_filtar_por_categoria_ao_listar_despesas_cadastradas(self):
        self.cadastrar_nova_despesa(
            descricao='Despesa Teste1')
        self.cadastrar_nova_despesa(
            descricao='Despesa Teste2')
        self.cadastrar_nova_despesa(
            descricao='Despesa Teste3')

        res = self.client.get(url + '?descricao=Despesa Teste2', format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

    def test_deve_listar_despesas_cadastradas_por_mes(self):
        self.cadastrar_nova_despesa(data=date(2022, 1, 1))
        self.cadastrar_nova_despesa(data=date(2022, 2, 1))

        res = self.client.get(url + '2022/2', format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

    def test_deve_atualizar_uma_despesa(self):
        self.cadastrar_nova_despesa()
        despesa = Despesa.objects.get()

        data = dict(
            descricao="Despesa Teste Atualizada",
            valor=Decimal('150'),
            data=date(2022, 1, 10)
        )

        pk = despesa.pk

        res = self.client.put(f'{url}{pk}/', data=data, format='json')

        despesa_atualizada = Despesa.objects.get()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(despesa_atualizada.descricao, data['descricao'])
        self.assertAlmostEqual(despesa_atualizada.valor, data['valor'])
        self.assertEqual(despesa_atualizada.data, data['data'])

    def test_deve_deletar_um_despesa(self):
        self.cadastrar_nova_despesa()
        despesa = Despesa.objects.get()

        pk = despesa.pk

        res = self.client.delete(f'{url}{pk}/', format='json')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
