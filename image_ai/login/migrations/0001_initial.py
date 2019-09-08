# Generated by Django 2.2.4 on 2019-09-04 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Cookie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('session_id', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('record_id', models.IntegerField(primary_key=True, serialize=False)),
                ('handImg', models.ImageField(upload_to='./upload/')),
                ('imgPredic', models.TextField(null=True)),
                ('imgDetect', models.ImageField(null=True, upload_to='')),
                ('time', models.TimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User')),
            ],
        ),
    ]
