# Generated by Django 4.2 on 2024-10-08 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performances', '0002_remove_performancelike_unique_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='styurl',
        ),
        migrations.AddField(
            model_name='performance',
            name='styurls',
            field=models.JSONField(blank=True, null=True),
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
