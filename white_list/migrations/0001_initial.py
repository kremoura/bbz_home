# Generated by Django 5.1.1 on 2024-10-02 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WhiteList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email_agente', models.EmailField(max_length=255)),
                ('nome_agente', models.CharField(max_length=255)),
                ('cid_condominio', models.IntegerField()),
                ('id_servico', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]