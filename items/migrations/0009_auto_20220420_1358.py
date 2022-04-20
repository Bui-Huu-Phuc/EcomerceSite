# Generated by Django 2.2.28 on 2022-04-20 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_item_image1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image1',
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/media/item-images'),
        ),
    ]
