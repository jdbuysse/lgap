# Generated by Django 2.2.5 on 2019-09-19 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TextInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='unique ID across all user texts', primary_key=True, serialize=False)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('text', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nlp.Text')),
            ],
        ),
    ]
