# Generated by Django 3.2.3 on 2021-10-13 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyzer',
            name='label_encoder',
            field=models.BinaryField(null=True),
        ),
        migrations.AddField(
            model_name='analyzer',
            name='word_vec',
            field=models.BinaryField(null=True),
        ),
    ]
