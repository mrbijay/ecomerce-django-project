# Generated by Django 3.2.7 on 2021-10-22 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('color', 'color'), ('size', 'size')], max_length=100),
        ),
    ]