# Generated by Django 4.0.2 on 2022-02-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text2html', '0003_editor_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='editor',
            name='date',
            field=models.DateField(auto_created=True, default=None),
        ),
    ]
