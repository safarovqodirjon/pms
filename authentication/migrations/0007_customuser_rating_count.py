# Generated by Django 4.2.1 on 2023-05-27 07:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0006_customuser_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="rating_count",
            field=models.IntegerField(default=0, verbose_name="Количество оценок"),
        ),
    ]
