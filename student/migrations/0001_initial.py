# Generated by Django 4.2.20 on 2025-05-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admitted_on', models.DateField(blank=True, null=True)),
                ('admission_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'student',
            },
        ),
    ]
