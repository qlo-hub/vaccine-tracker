# Generated by Django 3.1.7 on 2021-11-16 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0039_vaccine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccine',
            name='patient',
        ),
        migrations.CreateModel(
            name='PatientVaccine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.patient')),
                ('vaccine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.vaccine')),
            ],
        ),
    ]