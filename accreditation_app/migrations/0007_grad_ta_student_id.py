# Generated by Django 4.0.4 on 2022-06-29 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accreditation_app', '0006_doct_ta_grad_ta'),
    ]

    operations = [
        migrations.AddField(
            model_name='grad_ta',
            name='student_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.students'),
        ),
    ]