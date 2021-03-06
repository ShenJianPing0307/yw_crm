# Generated by Django 2.0 on 2019-05-17 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0039_auto_20190517_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productaudit',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='productaudit',
            name='product',
        ),
        migrations.AddField(
            model_name='productaudit',
            name='procedure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Procedure', verbose_name='订单-产品信息'),
        ),
        migrations.AlterField(
            model_name='procedure',
            name='audit_status',
            field=models.IntegerField(choices=[(1, '不合格'), (2, '合格')], default=1, verbose_name='产品审核状态'),
        ),
        migrations.AlterField(
            model_name='procedure',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Procedure', verbose_name='上一个流程'),
        ),
    ]
