# Generated by Django 4.0.4 on 2022-06-28 11:07

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('1', 'HOD'), ('2', 'Staff'), ('3', 'Student')], default=1, max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='academic_council',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('position', models.TextField(max_length=255)),
                ('address', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='board_of_governors',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('position', models.TextField(max_length=255)),
                ('address', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='board_of_studies',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('position', models.TextField(max_length=255)),
                ('address', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='doct_ta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('guide', models.TextField(default='', max_length=100)),
                ('area_of_work', models.TextField(max_length=1000)),
                ('year_of_registration', models.IntegerField(validators=[django.core.validators.MinValueValidator(2002), django.core.validators.MaxValueValidator(2022)])),
            ],
        ),
        migrations.CreateModel(
            name='finance_committee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('position', models.TextField(max_length=255)),
                ('address', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='grad_ta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('guide', models.TextField(default='', max_length=100)),
                ('specialization', models.TextField(max_length=1000)),
                ('year_of_registration', models.IntegerField(validators=[django.core.validators.MinValueValidator(1999), django.core.validators.MaxValueValidator(2022)])),
            ],
        ),
        migrations.CreateModel(
            name='iqac',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('position', models.TextField(max_length=255)),
                ('address', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='research_area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_completed', models.IntegerField(validators=[django.core.validators.MinValueValidator(1999), django.core.validators.MaxValueValidator(2022)])),
                ('title', models.TextField(max_length=1000)),
                ('spron_auth', models.TextField(max_length=255)),
                ('cost', models.BigIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='SessionYearModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_start_year', models.DateField()),
                ('session_end_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.courses')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(max_length=50)),
                ('profile_pic', models.FileField(upload_to='')),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='accreditation_app.courses')),
                ('session_year_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.sessionyearmodel')),
            ],
        ),
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_exam_marks', models.FloatField(default=0)),
                ('subject_assignment_marks', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.students')),
                ('subject_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Staffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(default='', max_length=255)),
                ('qualifications', models.CharField(default='', max_length=1000)),
                ('designation', models.TextField(default='', max_length=255)),
                ('area_of_specialisation', models.CharField(default='', max_length=1000)),
                ('experience', models.IntegerField(default=0)),
                ('number_of_doctorate_students_guided', models.BigIntegerField(default=0)),
                ('number_of_graduate_students_guided', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStaffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stafff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=255)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=255)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackStaffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attendance_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.attendance')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accreditation_app.students')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='session_year_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accreditation_app.sessionyearmodel'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accreditation_app.subjects'),
        ),
        migrations.CreateModel(
            name='AdminHOD',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]