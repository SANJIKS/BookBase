# Generated by Django 5.1.2 on 2024-10-15 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_receipt_userbookaccess_delete_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='book',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='books.book'),
            preserve_default=False,
        ),
    ]
