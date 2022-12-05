# Generated by Django 3.2.5 on 2021-07-09 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_info', '0004_note_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaign_info.city'),
        ),
        migrations.AlterField(
            model_name='npc',
            name='title',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
