# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-13 11:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20190412_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='goods',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='goods.Goods', verbose_name='商品'),
        ),
    ]
