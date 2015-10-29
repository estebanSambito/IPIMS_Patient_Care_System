# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import phonenumber_field.modelfields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('alert_level', models.IntegerField(default=0)),
                ('alert_description', models.CharField(null=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('doctor_first_name', models.CharField(default='', max_length=256)),
                ('doctor_last_name', models.CharField(default='', max_length=256)),
                ('doctor_type', models.CharField(default='Select Doctor Type', choices=[('Gynecologist', 'Gynecologist'), ('Neurologist', 'Neurologist'), ('Therapist', 'Therapist'), ('Allergist', 'Allergist'), ('Cardiologist', 'Cardiologist'), ('Dermatologist', 'Dermatologist'), ('Oncologist', 'Oncologist'), ('ENT', 'ENT'), ('Plastic Surgeon', 'Plastic Surgeon'), ('Psychiatrist', 'Psychiatrist'), ('Urologist', 'Urologist'), ('Podiatrist', 'Podiatrist')], max_length=256)),
                ('doctor_user', models.OneToOneField(to=settings.AUTH_USER_MODEL, default='')),
            ],
        ),
        migrations.CreateModel(
            name='EMedication',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('medication_name', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('approved', models.IntegerField(default=0)),
                ('alertSent', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PatientAppt',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.CharField(unique=True, max_length=1000)),
                ('pain_level', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('medical_conditions', models.CharField(default='None', max_length=1000)),
                ('allergies', models.CharField(default='None', max_length=1000)),
                ('resolved', models.IntegerField(default=0, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientHealthConditions',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nausea_level', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('hunger_level', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('anxiety_level', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('stomach_level', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('body_ache_level', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('chest_pain_level', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('user', models.OneToOneField(to='ipcms.Patient', default='', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='patientMedicalReport',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('first_name', models.CharField(default='', max_length=256)),
                ('last_name', models.CharField(default='', max_length=256)),
                ('age', models.IntegerField(default=18)),
                ('gender', models.CharField(default='Select a gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer not to say', 'Prefer Not To Say')], max_length=256)),
                ('race', models.CharField(default='Other', choices=[('white', 'White'), ('american_indian_alaskan_native', 'American Indian or Alaskan Native'), ('hawaiian', 'Native Hawaiian or Other Pacific Islander'), ('black', 'Black or African American'), ('asian', 'Asian'), ('other', 'Other')], max_length=256)),
                ('DOB', models.DateField(default='')),
                ('allergies', models.CharField(default='', max_length=256)),
                ('medications', models.CharField(default='', max_length=256)),
                ('insurance_provider', models.CharField(max_length=256)),
                ('insurance_policy_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PermissionsRole',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('role', models.CharField(choices=[('admin', 'admin'), ('nurse', 'nurse'), ('staff', 'staff'), ('doctor', 'doctor'), ('patient', 'patient'), ('lab', 'lab')], max_length=256)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, default='', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TempPatientData',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('email_address', models.CharField(max_length=256)),
                ('first_name', models.CharField(default='', max_length=256)),
                ('last_name', models.CharField(default='', max_length=256)),
                ('age', models.IntegerField(default=18)),
                ('gender', models.CharField(default='Select a gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer not to say', 'Prefer Not To Say')], max_length=256)),
                ('race', models.CharField(default='Other', choices=[('white', 'White'), ('american_indian_alaskan_native', 'American Indian or Alaskan Native'), ('hawaiian', 'Native Hawaiian or Other Pacific Islander'), ('black', 'Black or African American'), ('asian', 'Asian'), ('other', 'Other')], max_length=256)),
                ('income', models.CharField(default='Prefer Not To Say', choices=[('$0-$10,000', '$0-$10,000'), ('$10,001-$30,000', '$10,001-$30,000'), ('$30,001-$60,000', '$30,001-$60,000'), ('$60,001-$85,000', '$60,001-$85,000'), ('$85,001-$110,000', '$85,001-$110,000'), ('$110,001+', '$110,001+'), ('Prefer Not To Say', 'Prefer Not To Say')], max_length=256)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='', blank=True, max_length=128)),
                ('DOB', models.DateField(default='')),
                ('ssn', models.IntegerField()),
                ('allergies', models.CharField(default='', max_length=256)),
                ('address', models.CharField(default='', max_length=256)),
                ('medications', models.CharField(default='', max_length=256)),
                ('insurance_provider', models.CharField(max_length=256)),
                ('insurance_policy_number', models.IntegerField()),
                ('data_sent', models.IntegerField(default=0)),
                ('user', models.OneToOneField(default='', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='patientappt',
            name='current_health_conditions',
            field=models.ForeignKey(default='', to='ipcms.PatientHealthConditions', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='patientappt',
            name='doctor',
            field=models.ForeignKey(default=-1, to='ipcms.Doctor'),
        ),
        migrations.AddField(
            model_name='patientappt',
            name='user',
            field=models.ForeignKey(to='ipcms.Patient', default='', blank=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='fill_from_application',
            field=models.OneToOneField(default='', to='ipcms.TempPatientData', null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(default='', to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='emedication',
            name='patient',
            field=models.OneToOneField(to='ipcms.Patient', default=''),
        ),
        migrations.AddField(
            model_name='alert',
            name='alert_patient',
            field=models.OneToOneField(to='ipcms.Patient', null=True),
        ),
    ]
