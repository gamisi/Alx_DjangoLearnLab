# Generated by Django 4.2.19 on 2025-02-23 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0005_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': [('can_add_book', 'Can add a new book'), ('can_change_book', 'Can change an existing book'), ('can_delete_book', 'Can delete a book')]},
        ),
    ]
