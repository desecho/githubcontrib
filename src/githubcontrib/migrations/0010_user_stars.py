# Generated by Django 4.0.4 on 2022-05-21 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('githubcontrib', '0009_alter_user_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stars',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
