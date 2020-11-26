# Generated by Django 3.0.8 on 2020-11-10 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20201107_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('charge', models.CharField(blank=True, max_length=32, null=True)),
                ('username', models.CharField(blank=True, max_length=150, null=True)),
                ('team', models.CharField(blank=True, max_length=32, null=True)),
                ('position', models.CharField(blank=True, max_length=32, null=True)),
                ('email', models.CharField(blank=True, max_length=254, null=True)),
                ('grade', models.CharField(blank=True, max_length=32, null=True)),
                ('phone', models.CharField(blank=True, max_length=128, null=True)),
                ('date_joined', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]