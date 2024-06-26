# Generated by Django 5.0.4 on 2024-04-19 22:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CareTaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('doctor', 'Doctor'), ('resident', 'Resident'), ('livechart', 'Live Chart'), ('cardiology', 'Cardiology')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('admission_datetime', models.DateTimeField()),
                ('care_plan', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_type', models.CharField(choices=[('doctor', 'Doctor'), ('resident', 'Resident'), ('lab_result', 'Lab Result'), ('care_plan', 'Care Plan'), ('generated_care_plan', 'AI Generated Care Plan'), ('consult', 'Consult Response')], max_length=255)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('is_enabled', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icu.caretaker')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icu.patient')),
            ],
        ),
    ]
