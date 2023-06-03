from django.db import migrations
from ..models import CustomUser

def forwards_func(apps, schema_editor):
    users = CustomUser.objects.all()
    for user in users:
        user.set_password(user.password)
        user.save(update_fields=["password"])


class Migration(migrations.Migration):

    dependencies = [
        ('accreditation_app', '0034_alter_research_area_year_completed_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]