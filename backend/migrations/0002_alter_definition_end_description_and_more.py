# Generated by Django 4.1.7 on 2023-03-31 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='end_description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='definition',
            name='filename',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='definition',
            name='gender',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='definition',
            name='other_category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='definition',
            name='region',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='definition',
            name='specialty',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='definition',
            name='use',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
