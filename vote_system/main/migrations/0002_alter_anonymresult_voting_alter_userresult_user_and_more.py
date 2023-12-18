# Generated by Django 4.2.7 on 2023-12-18 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymresult',
            name='voting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.voting'),
        ),
        migrations.AlterField(
            model_name='userresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userresult',
            name='voting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.voting'),
        ),
    ]
