# Generated by Django 5.1.2 on 2024-10-29 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='content',
            field=models.FileField(blank=True, null=True, upload_to='books/content/'),
        ),
    ]