# Generated by Django 5.1 on 2024-08-18 11:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloggenerator', '0004_alter_blogpost_youtube_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]