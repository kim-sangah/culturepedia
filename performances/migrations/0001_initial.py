# Generated by Django 4.2 on 2024-10-17 13:14

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
            name='Facility',
            fields=[
                ('kopis_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('seatscale', models.IntegerField(null=True)),
                ('relateurl', models.TextField(null=True)),
                ('address', models.TextField(null=True)),
                ('telno', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('kopis_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=20)),
                ('start_date', models.CharField(max_length=100)),
                ('end_date', models.CharField(max_length=100)),
                ('facility_name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('synopsis', models.TextField(blank=True, null=True)),
                ('cast', models.CharField(max_length=100, null=True)),
                ('crew', models.CharField(max_length=100, null=True)),
                ('runtime', models.CharField(max_length=100, null=True)),
                ('age', models.CharField(max_length=100, null=True)),
                ('production', models.CharField(max_length=200, null=True)),
                ('agency', models.CharField(max_length=200, null=True)),
                ('pricing', models.TextField(null=True)),
                ('visit', models.CharField(max_length=2)),
                ('daehakro', models.CharField(max_length=2)),
                ('festival', models.CharField(max_length=2)),
                ('musicallicense', models.CharField(max_length=2)),
                ('musicalcreate', models.CharField(max_length=2)),
                ('dtguidance', models.TextField(null=True)),
                ('poster', models.TextField(null=True)),
                ('styurls', models.JSONField(blank=True, null=True)),
                ('facility_kopis_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='performance_facility', to='performances.facility')),
            ],
        ),
        migrations.CreateModel(
            name='Performlist',
            fields=[
                ('kopis_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('facility_name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100, null=True)),
                ('start_date', models.CharField(max_length=20)),
                ('end_date', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perform_reviews', to='performances.performance')),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_likes', to='performances.performance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('performance_api_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_hashtag', to='performances.performance')),
            ],
        ),
    ]
