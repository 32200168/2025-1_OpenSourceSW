# Generated by Django 5.2.1 on 2025-06-03 07:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('music', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('users', models.ManyToManyField(related_name='hashtag_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('hashtags', models.ManyToManyField(blank=True, related_name='playlists', to='playlist.hashtag')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistHashtagScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlist.hashtag')),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlist.playlist')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.song')),
            ],
            options={
                'unique_together': {('playlist', 'song')},
            },
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(related_name='playlists', through='playlist.PlaylistSong', to='music.song'),
        ),
        migrations.CreateModel(
            name='PlaylistTaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtags', models.ManyToManyField(related_name='playlist_tastes', through='playlist.PlaylistHashtagScore', to='playlist.hashtag')),
                ('playlist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='playlist.playlist')),
            ],
        ),
        migrations.AddField(
            model_name='playlisthashtagscore',
            name='playlist_taste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlist.playlisttaste'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlist.playlist')),
            ],
            options={
                'unique_together': {('playlist', 'user')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='playlisthashtagscore',
            unique_together={('playlist_taste', 'hashtag')},
        ),
    ]
