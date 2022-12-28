from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from receitas.models import Receita
from datetime import date
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

url = reverse('receita-list')


class ReceitaTest(APITestCase):
    username = "test_user"
    password = "123456"

    @classmethod
    def setUpClass(cls) -> None:
        super(ReceitaTest, cls).setUpClass()

        User = get_user_model()

        user = User.objects.create(
            username=cls.username,
            password=cls.password
        )

        refresh = RefreshToken.for_user(user)

        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        cls.api_client = client

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

    def test_deve_cadastrar_nova_receita(self):
        receita = dict(
            descricao="Receita Teste",
            valor=Decimal('100'),
            data=date(2022, 1, 1)
        )

        res = self.api_client.post(url, receita, format='json')

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

        self.api_client.post(url, receita_1, format='json')

        res = self.api_client.post(url, receita_2, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deve_listar_receitas_cadastradas(self):
        self.cadastrar_nova_receita()

        res = self.api_client.get(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

    def test_deve_filtar_por_categoria_ao_listar_receitas_cadastradas(self):
        self.cadastrar_nova_receita(
            descricao='Receita Teste1')
        self.cadastrar_nova_receita(
            descricao='Receita Teste2')
        self.cadastrar_nova_receita(
            descricao='Receita Teste3')

        res = self.api_client.get(
            url + '?descricao=Receita Teste2', format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)

    def test_deve_listar_receitas_cadastradas_por_mes(self):
        self.cadastrar_nova_receita(data=date(2022, 1, 1))
        self.cadastrar_nova_receita(data=date(2022, 2, 1))

        res = self.api_client.get(url + '2022/2', format='json')

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

        res = self.api_client.put(f'{url}{pk}/', data=data, format='json')

        receita_atualizada = Receita.objects.get()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(receita_atualizada.descricao, data['descricao'])
        self.assertAlmostEqual(receita_atualizada.valor, data['valor'])
        self.assertEqual(receita_atualizada.data, data['data'])

    def test_deve_deletar_um_receita(self):
        self.cadastrar_nova_receita()
        receita = Receita.objects.get()

        pk = receita.pk

        res = self.api_client.delete(f'{url}{pk}/', format='json')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
