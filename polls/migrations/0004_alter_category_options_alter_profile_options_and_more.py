# Generated by Django 5.1.1 on 2024-12-02 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_answer_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name_plural': 'Вопросы'},
        ),
    ]
