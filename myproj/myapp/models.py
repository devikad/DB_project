# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
# * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
   # user = models.OneToOneField(User)
    user_id = models.BigIntegerField(primary_key=True)
   # first_name = models.CharField(max_length=40, blank=True)
   # last_name = models.CharField(max_length=40, blank=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True)
   # email = models.CharField(max_length=40)  # not null
    phone_number = models.BigIntegerField(blank=True, null=True)
    lives_in_location = models.BigIntegerField()
#    password = models.CharField(max_length=20)  # not null
    about_me = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
    #    managed = False
        db_table = 'app_user'

#User.profile = property(lambda u: AppUser.objects.get_or_create(user=u)[0])


class BelongsTo(models.Model):
    belongsto_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(AppUser)
    group = models.ForeignKey('UserGroup')

    class Meta:
        managed = False
        db_table = 'belongs_to'


class CanSpeak(models.Model):
    canspeak_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(AppUser)
    language = models.ForeignKey('Language')
    familiarity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'can_speak'


class Comments(models.Model):
    comments_id = models.BigIntegerField(primary_key=True)
    text = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'comments'


class Company(models.Model):
    company_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    field = models.CharField(max_length=40)
    about = models.CharField(max_length=2048, blank=True)
    no_of_employees = models.BigIntegerField(blank=True, null=True)
    web_address = models.CharField(max_length=40, blank=True)
    established_year = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        managed = False
        db_table = 'company'


class CompanyLocatedIn(models.Model):
    companylocation_id = models.BigIntegerField(primary_key=True)
    company = models.ForeignKey(Company)
    location = models.ForeignKey('Location')

    class Meta:
        managed = False
        db_table = 'company_located_in'


class HasInterest(models.Model):
    hasinterest_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(AppUser)
    interest = models.ForeignKey('Interest')
    degree_of_interest = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'has_interest'


class HasRelation(models.Model):
    hasrelation_id = models.BigIntegerField(primary_key=True)
    relation_type = models.ForeignKey('RelationType')
    user_1 = models.ForeignKey(AppUser, related_name='user1')
    user_2 = models.ForeignKey(AppUser, related_name='user2')

    class Meta:
        managed = False
        db_table = 'has_relation'


class Interest(models.Model):
    interest_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        managed = False
        db_table = 'interest'


class IsTopic(models.Model):
    istopic_id = models.BigIntegerField(primary_key=True)
    interest = models.ForeignKey(Interest)
    group = models.ForeignKey('UserGroup')

    class Meta:
        managed = False
        db_table = 'is_topic'


class Language(models.Model):
    language_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        managed = False
        db_table = 'language'


class Location(models.Model):
    location_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        managed = False
        db_table = 'location'


class MakeComment(models.Model):
    makecomment_id = models.BigIntegerField(primary_key=True)
    posting_time = models.DateTimeField()
    group = models.ForeignKey('UserGroup')
    user = models.ForeignKey(AppUser)
    comment = models.ForeignKey(Comments)

    class Meta:
        managed = False
        db_table = 'make_comment'


class RelationType(models.Model):
    relationtype_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        managed = False
        db_table = 'relation_type'


class StudiesIn(models.Model):
    studiesin_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(AppUser)
    university = models.ForeignKey('University')
    major = models.CharField(max_length=40, blank=True)
    degree = models.IntegerField(blank=True, null=True)
    location = models.ForeignKey(Location)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'studies_in'


class University(models.Model):
    university_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=400)
    web_address = models.CharField(max_length=1024, blank=True)
    established_year = models.BigIntegerField(blank=True, null=True)
    about = models.CharField(max_length=2048, blank=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        managed = False
        db_table = 'university'


class UniversityLocatedIn(models.Model):
    universitylocation_id = models.BigIntegerField(primary_key=True)
    university = models.ForeignKey(University)
    location = models.ForeignKey(Location)

    class Meta:
        managed = False
        db_table = 'university_located_in'


class UserGroup(models.Model):
    usergroup_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    about = models.CharField(max_length=400)
    admin = models.ForeignKey(AppUser, db_column='admin')

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        managed = False
        db_table = 'user_group'


class WorksIn(models.Model):
    worksin_id = models.BigIntegerField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=40, blank=True)
    project = models.CharField(max_length=40, blank=True)
    user = models.ForeignKey(AppUser)
    company = models.ForeignKey(Company)
    location = models.ForeignKey(Location)

    class Meta:
        managed = False
        db_table = 'works_in'
