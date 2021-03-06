# Generated by Django 2.0 on 2019-05-12 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0022_auto_20190512_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='product',
        ),
        migrations.AddField(
            model_name='customer',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Product', verbose_name='咨询的产品'),
        ),
        migrations.AlterField(
            model_name='procedure',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Procedure', verbose_name='上一个流程'),
        ),
    ]
