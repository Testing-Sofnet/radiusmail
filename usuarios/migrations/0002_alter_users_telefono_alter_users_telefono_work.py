# Generated by Django 4.1.1 on 2022-09-13 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='telefono',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='telefono_work',
            field=models.CharField(max_length=11, null=True),
        ),
    ]