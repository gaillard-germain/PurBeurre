# Generated by Django 3.1.7 on 2021-05-05 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0008_auto_20210430_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_modified_t',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
