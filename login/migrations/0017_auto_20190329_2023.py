# Generated by Django 2.1.5 on 2019-03-29 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_auto_20190329_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(null=True, upload_to='photo/'),
        ),
    ]