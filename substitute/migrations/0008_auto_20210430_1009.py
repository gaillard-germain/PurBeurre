# Generated by Django 3.1.7 on 2021-04-30 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0007_auto_20210430_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]