# Generated by Django 2.0.2 on 2018-02-04 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghcontrib', '0004_commit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commit',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='repo',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='user',
            name='homepage',
        ),
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('ru', 'Русский')], default='en', max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
