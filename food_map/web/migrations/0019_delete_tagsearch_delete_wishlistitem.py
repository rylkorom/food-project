# Generated by Django 4.0.1 on 2022-01-27 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_alter_location_options_restaurant_tags_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TagSearch',
        ),
        migrations.DeleteModel(
            name='WishListItem',
        ),
    ]
