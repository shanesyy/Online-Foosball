# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-24 18:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameProfileEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('team', models.IntegerField(default=1)),
                ('score', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('valid', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('first_in', models.BooleanField(default=True)),
                ('result', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GameStateEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score1', models.IntegerField()),
                ('score2', models.IntegerField()),
                ('ball_init_angle_index', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=200, null=True)),
                ('picture', models.FileField(blank=True, default='images/anonymous.png', upload_to='images')),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('content_type', models.CharField(max_length=50)),
                ('total_scores', models.IntegerField()),
                ('following', models.ManyToManyField(related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_num', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('s1', 'room available'), ('s2', 'room full'), ('s3', 'ready'), ('s4', 'in game')], default='s1', max_length=2)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_room', to=settings.AUTH_USER_MODEL)),
                ('player', models.ManyToManyField(related_name='room', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScoreEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='score', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WaitUserEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waitlist', to='foosball.RoomEntry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='scores',
            field=models.ManyToManyField(to='foosball.ScoreEntry'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='own', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gamestateentry',
            name='game_room',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='game_state', to='foosball.RoomEntry'),
        ),
        migrations.AddField(
            model_name='gameprofileentry',
            name='game_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='players_info', to='foosball.RoomEntry'),
        ),
        migrations.AddField(
            model_name='gameprofileentry',
            name='guest',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guest_game_info', to='foosball.GameProfileEntry'),
        ),
        migrations.AddField(
            model_name='gameprofileentry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_info', to=settings.AUTH_USER_MODEL),
        ),
    ]