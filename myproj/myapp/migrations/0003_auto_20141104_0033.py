# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20141104_0025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appuser',
            old_name='appuser_id',
            new_name='user_id',
        ),
    ]
