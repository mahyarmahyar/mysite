# Generated by Django 5.0.2 on 2024-03-13 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_contact_post_counted_views_post_created_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
