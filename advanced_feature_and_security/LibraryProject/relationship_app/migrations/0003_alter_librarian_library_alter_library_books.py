# Generated by Django 4.2.19 on 2025-02-22 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0002_alter_librarian_library_alter_library_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarian',
            name='library',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='librarians', to='relationship_app.library'),
        ),
        migrations.AlterField(
            model_name='library',
            name='books',
            field=models.ManyToManyField(related_name='library', to='relationship_app.book'),
        ),
    ]
