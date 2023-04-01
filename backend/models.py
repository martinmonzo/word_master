from django.db import models

# Create your models here.
class Definition(models.Model):
    meaning = models.TextField()
    answer = models.CharField(max_length=255)
    region = models.CharField(max_length=100, null=True)
    grammatical_category = models.CharField(max_length=100)
    specialty = models.CharField(max_length=10, null=True)
    is_easy = models.BooleanField(default=False)
    is_very_hard = models.BooleanField(default=False)
    filename = models.CharField(max_length=100, null=True)
    other_category = models.CharField(max_length=100, null=True)
    is_colloquial = models.BooleanField()
    is_pronominal = models.BooleanField()
    is_plural = models.BooleanField()
    use = models.CharField(max_length=10, null=True)
    end_description = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, null=True)
    is_recursive = models.BooleanField()


class Encyclopedic(models.Model):
    description = models.TextField()
    answer = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    is_easy = models.BooleanField(default=False)
    is_very_hard = models.BooleanField(default=False)
