# Generated by Django 2.2.1 on 2019-05-30 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_auto_20181231_0628'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='predicted_winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predicted_wins', to='server.Team'),
        ),
    ]
