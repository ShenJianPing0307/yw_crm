# Generated by Django 2.0 on 2019-05-17 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0041_auto_20190517_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedure',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Procedure', verbose_name='上一个流程'),
        ),
        migrations.AlterField(
            model_name='productaudit',
            name='procedure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Procedure', verbose_name='订单-产品信息'),
        ),
    ]