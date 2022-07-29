# Generated by Django 4.0.4 on 2022-07-02 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accreditation_app', '0011_research_area'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffs',
            name='address',
        ),
        migrations.AddField(
            model_name='staffs',
            name='area_of_specialisation',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='staffs',
            name='designation',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='staffs',
            name='experience',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='staffs',
            name='name',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='staffs',
            name='number_of_doctorate_students_guided',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='staffs',
            name='number_of_graduate_students_guided',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='staffs',
            name='qualifications',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
