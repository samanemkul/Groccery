# Generated by Django 5.0.6 on 2024-07-31 10:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groccery', '0003_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='phone',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='groccery.category', verbose_name='Product Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/Images', verbose_name='Product Image'),
        ),
    ]
