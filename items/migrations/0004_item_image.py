# Generated by Django 2.2.28 on 2022-04-20 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_remove_item_image4'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/media/item-images'),
        ),
    ]
