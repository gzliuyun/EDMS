# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcademicInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=255, db_index=True)

    # TODO 如有需要为name字段添加索引
    name = models.CharField(max_length=255, blank=True, null=True)
    amount1 = models.IntegerField(blank=True, null=True)
    amount2 = models.IntegerField(blank=True, null=True)
    h_index = models.IntegerField(blank=True, null=True)
    core = models.CharField(max_length=255, blank=True, null=True)
    cssci = models.CharField(max_length=255, blank=True, null=True)
    rdfybkzl = models.CharField(max_length=255, blank=True, null=True)

    # TODO co_expert更改为ForeignKey字段
    # co_expert = models.ForeignKey(BasicInfo, blank=True, null=True)
    co_expert = models.CharField(max_length=255, blank=True, null=True)
    co_agency = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'academic_info'

    def __str__(self):
        return self.name + " h_index: " + str(self.h_index)


class BasicInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    # TODO 如有需要为name字段添加索引
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    theme_list = models.CharField(max_length=255, blank=True, null=True)
    sub_list = models.CharField(max_length=255, blank=True, null=True)
    resume = models.TextField(blank=True, null=True)
    img_url = models.CharField(max_length=255, blank=True, null=True)
    url1 = models.CharField(max_length=255, blank=True, null=True)
    url2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'basic_info'
        verbose_name = '专家基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name + " " + self.university


class ExpertIntro(models.Model):

    # TODO 如有需要为name字段添加索引
    name = models.CharField(max_length=255, db_index=True)
    university = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    profile = models.TextField()
    image_url = models.CharField(max_length=255, blank=True, null=True)
    info_url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'expert_intro'

    def __str__(self):
        return self.name + " " + self.profile


class OpinionInfo(models.Model):
    content = models.TextField(blank=True, null=True)
    expert = models.ForeignKey(BasicInfo, models.DO_NOTHING, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opinion_info'

    def __str__(self):
        return self.expert + " " + self.content


class PaperInfo(models.Model):
    paper_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    authors = models.CharField(max_length=255, blank=True, null=True)
    author1 = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    author2 = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    author3 = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    author4 = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    author5 = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    # TODO author1~author5更改为authors ForeignKey字段
    # author = models.ForeignKey(BasicInfo, blank=True, bull=True)

    class Meta:
        managed = True
        db_table = 'paper_info'

    def __str__(self):
        return self.title + " " + self.authors
