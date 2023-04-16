# Generated by Django 4.2 on 2023-04-10 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='description',
            field=models.CharField(blank=True, max_length=4096),
        ),
        migrations.AlterField(
            model_name='mission',
            name='end_date',
            field=models.DateTimeField(blank=True, verbose_name='Date of completion'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='start_date',
            field=models.DateTimeField(blank=True, verbose_name='Date of commencement'),
        ),
    ]
