# Generated by Django 2.1.7 on 2019-04-28 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_auto_20190428_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_question',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='questions.Question'),
        ),
    ]