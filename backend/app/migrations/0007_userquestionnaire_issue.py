# Generated by Django 5.1 on 2024-09-05 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_userquestionnaire_problem'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquestionnaire',
            name='issue',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
