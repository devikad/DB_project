# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('user_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=40, blank=True)),
                ('last_name', models.CharField(max_length=40, blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(max_length=1, blank=True)),
                ('email', models.CharField(max_length=40)),
                ('phone_number', models.BigIntegerField(null=True, blank=True)),
                ('lives_in_location', models.BigIntegerField()),
                ('password', models.CharField(max_length=20)),
                ('about_me', models.CharField(max_length=400, blank=True)),
            ],
            options={
                'db_table': 'app_user',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BelongsTo',
            fields=[
                ('belongsto_id', models.BigIntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'belongs_to',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CanSpeak',
            fields=[
                ('canspeak_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('familiarity', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'can_speak',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comments_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'comments',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('field', models.CharField(max_length=40)),
                ('about', models.CharField(max_length=2048, blank=True)),
                ('no_of_employees', models.BigIntegerField(null=True, blank=True)),
                ('web_address', models.CharField(max_length=40, blank=True)),
                ('established_year', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'company',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyLocatedIn',
            fields=[
                ('companylocation_id', models.BigIntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'company_located_in',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HasInterest',
            fields=[
                ('hasinterest_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('degree_of_interest', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'has_interest',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HasRelation',
            fields=[
                ('hasrelation_id', models.BigIntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'has_relation',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('interest_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'interest',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IsTopic',
            fields=[
                ('istopic_id', models.BigIntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'is_topic',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('language_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'language',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'location',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MakeComment',
            fields=[
                ('makecomment_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('posting_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'make_comment',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('relationtype_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'relation_type',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudiesIn',
            fields=[
                ('studiesin_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('major', models.CharField(max_length=40, blank=True)),
                ('degree', models.IntegerField(null=True, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'studies_in',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('university_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=400)),
                ('web_address', models.CharField(max_length=1024, blank=True)),
                ('established_year', models.BigIntegerField(null=True, blank=True)),
                ('about', models.CharField(max_length=2048, blank=True)),
            ],
            options={
                'db_table': 'university',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UniversityLocatedIn',
            fields=[
                ('universitylocation_id', models.BigIntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'university_located_in',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('usergroup_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('about', models.CharField(max_length=400)),
            ],
            options={
                'db_table': 'user_group',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorksIn',
            fields=[
                ('worksin_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('position', models.CharField(max_length=40, blank=True)),
                ('project', models.CharField(max_length=40, blank=True)),
            ],
            options={
                'db_table': 'works_in',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
