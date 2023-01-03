# Generated by Django 4.1.4 on 2023-01-03 02:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaign_info', '0001_squashed_0006_alter_npc_campaigns'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='join_code',
            field=models.CharField(default='', max_length=6, unique=True),
        ),
        migrations.CreateModel(
            name='CampaignRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_dm', models.BooleanField()),
                ('campaign', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='campaign_info.campaign')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
