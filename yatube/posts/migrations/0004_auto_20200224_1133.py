# Generated by Django 2.2 on 2020-02-24 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20200214_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='rules',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]