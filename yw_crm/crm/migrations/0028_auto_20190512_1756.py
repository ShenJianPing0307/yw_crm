# Generated by Django 2.0 on 2019-05-12 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0027_auto_20190512_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedure',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Procedure', verbose_name='上一个流程'),
        ),
        migrations.AlterField(
            model_name='productaudit',
            name='audit_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
