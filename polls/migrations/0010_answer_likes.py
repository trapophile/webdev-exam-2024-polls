# Generated by Django 5.1.1 on 2024-12-13 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_alter_answer_usefull_historicalanswer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(related_name='likes_answer', to='polls.profile', verbose_name='Лайки'),
        ),
    ]
