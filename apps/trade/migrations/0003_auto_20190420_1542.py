# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-04-20 15:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20190420_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good', to='goods.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.OrderInfo', verbose_name='订单信息'),
        ),
    ]
