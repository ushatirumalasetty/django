# Generated by Django 2.0.2 on 2020-03-16 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practise', '0002_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateField(verbose_name='date published'),
        ),
    ]
