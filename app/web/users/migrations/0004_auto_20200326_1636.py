# Generated by Django 2.2.10 on 2020-03-26 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Beheerder'), (5, 'Persoonlijk begeleider')], default=1, verbose_name='Gebruiker type'),
        ),
    ]
