# Generated by Django 3.2 on 2021-05-23 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idx_search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexitem',
            name='search_string',
            field=models.TextField(db_index=True),
        ),
    ]
