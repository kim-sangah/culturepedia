# Generated by Django 4.2 on 2024-10-20 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='performance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perform_reviews', to='performances.performance'),
        ),
    ]
