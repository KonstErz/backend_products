# Generated by Django 3.1.2 on 2020-10-08 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(help_text='Product name', max_length=200),
        ),
    ]
