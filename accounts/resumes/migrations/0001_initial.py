# Generated by Django 3.2.7 on 2021-09-16 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('job_title', models.CharField(max_length=100)),
            ],
        ),
    ]
