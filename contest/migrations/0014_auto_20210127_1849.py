# Generated by Django 3.1.4 on 2021-01-27 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0013_auto_20210127_1846'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestrating',
            options={'ordering': ['-solved_count', '-penalty']},
        ),
    ]
