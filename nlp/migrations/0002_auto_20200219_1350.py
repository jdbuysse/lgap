# Generated by Django 2.2.5 on 2020-02-19 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nlp', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.RemoveField(
            model_name='bytetext',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.AlterField(
            model_name='uploadtext',
            name='fulltext',
            field=models.TextField(max_length=2000000),
        ),
        migrations.DeleteModel(
            name='ByteText',
        ),
    ]
