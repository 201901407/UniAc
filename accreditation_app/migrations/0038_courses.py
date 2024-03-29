# Generated by Django 4.1.1 on 2023-10-29 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accreditation_app', '0037_uploadedfileshistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.TextField(default='')),
                ('course_id', models.TextField(default='', max_length=6)),
                ('enrolled_students', models.BigIntegerField(default=0)),
                ('course_instructor', models.ManyToManyField(to='accreditation_app.staffs')),
                ('involved_ta', models.ManyToManyField(to='accreditation_app.ta')),
            ],
        ),
    ]
