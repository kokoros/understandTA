# Generated by Django 2.1.5 on 2019-04-23 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20190421_2324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pets',
            options={'ordering': ['id']},
        ),
    ]