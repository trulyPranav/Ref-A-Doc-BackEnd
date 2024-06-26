# Generated by Django 5.0.4 on 2024-04-13 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('age', models.IntegerField(default=0)),
                ('user_type', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='Oth', max_length=10)),
                ('phone_number', models.CharField(default='0', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=100)),
                ('availability', models.BooleanField(default=False)),
                ('hospital', models.CharField(max_length=100)),
                ('phone_number', models.CharField(default='0', max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='users.customuser')),
            ],
        ),
    ]
