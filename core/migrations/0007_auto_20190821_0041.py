# Generated by Django 2.2.1 on 2019-08-20 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190820_2341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='num_vote_down',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='num_vote_up',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='vote_score',
        ),
    ]