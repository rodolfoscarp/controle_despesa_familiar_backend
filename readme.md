# Controle de Depesas Familiares

Api de Controle de despesas e receitas familiares.

### Requisitos

- docker
- docker-compose

### Como usar

- Construir imagens e levantar os containers.
  `docker-compose up`

- Fazer as Migrações Django
  `docker-compose exec webapp python manage.py migrate`

- Criar o usuario administrador Django
  `docker-compose exec webapp python manage.py createsuperuser`

- Coletar arquivos estaticos:
  `docker-compose exec webapp python manage.py collectstatic`

A Api pode ser acessada pela porta _8000_.

### Documentação

Documentação gerada utilizando o pacote [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/)

- **Swagger**

  - http://127.0.0.1:8000/swagger/

- **Redoc**
  - http://127.0.0.1:8000/redoc/
