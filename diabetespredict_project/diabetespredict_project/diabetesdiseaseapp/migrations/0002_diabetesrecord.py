# Generated by Django 5.2 on 2025-05-09 06:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diabetesdiseaseapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiabetesRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pregnancies', models.PositiveIntegerField()),
                ('Glucose', models.FloatField()),
                ('BloodPressure', models.FloatField()),
                ('SkinThickness', models.FloatField()),
                ('Insulin', models.FloatField()),
                ('BMI', models.FloatField()),
                ('DiabetesPedigreeFunction', models.FloatField()),
                ('Age', models.PositiveIntegerField()),
                ('prediction_result', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
