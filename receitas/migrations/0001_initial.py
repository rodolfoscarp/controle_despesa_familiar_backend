# Generated by Django 4.1.4 on 2022-12-13 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Receita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('descricao', models.CharField(max_length=255, verbose_name='descricao')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='valor')),
                ('data', models.DateField(verbose_name='data')),
            ],
        ),
    ]
