# Generated by Django 3.2.5 on 2021-11-22 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_fileentitymodel_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileentitymodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
