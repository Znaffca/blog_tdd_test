# Generated by Django 2.2.2 on 2019-06-19 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("blog", "0002_auto_20190616_1740")]

    operations = [
        migrations.AddField(
            model_name="entry", name="slug", field=models.SlugField(default="")
        )
    ]
