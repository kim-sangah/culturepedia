# Generated by Django 4.2 on 2024-10-02 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('performances', '0002_facility_performance_article_like_review_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='age',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='cast',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='crew',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='daehakro',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='dtguidance',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='entprsmnP',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='entrprsnmA',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='festival',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='musicalcreate',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='musicallicense',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='pricing',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='runtime',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='synopsis',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='visit',
        ),
    ]
