# Generated by Django 5.1.1 on 2024-10-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='timestamp',
            new_name='criacao',
        ),
        migrations.AddField(
            model_name='log',
            name='timezone',
            field=models.CharField(default='UTC', max_length=50),
        ),
        migrations.AddField(
            model_name='log',
            name='ultima_atualizacao',
            field=models.DateTimeField(auto_now=True),
        ),
    ]