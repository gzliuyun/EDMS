# Generated by Django 2.1 on 2018-09-12 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0007_auto_20180904_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicinfo',
            name='id',
            field=models.CharField(db_index=True, max_length=255, primary_key=True, serialize=False),
        ),
    ]