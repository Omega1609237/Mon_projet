# Generated by Django 5.1.7 on 2025-05-02 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entreprises', '0003_candidature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidature',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='cvs/'),
        ),
    ]
