# Generated by Django 5.1.1 on 2024-10-02 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_remove_log_timezone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
