# Generated by Django 5.1 on 2024-08-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloggenerator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='transcript',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='youtube_link',
            field=models.TextField(),
        ),
    ]