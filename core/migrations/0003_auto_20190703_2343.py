# Generated by Django 2.2.3 on 2019-07-03 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190703_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rcuser',
            name='gang',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Gang'),
        ),
    ]
