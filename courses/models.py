from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name

class ItemBase(models.Model):
    class Meta:
        abstract = True
    subject = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject


class Course(ItemBase):
    class Meta:
        unique_together = ['subject', 'category']
        ordering = ["-id"]
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)


class Lesson(ItemBase):
    class Meta:
        unique_together = ['subject', 'course']
    content = RichTextField()
    course = models.ForeignKey(Course,related_name="lessons" , on_delete=models.CASCADE, null=True, blank=True)
    tags= models.ManyToManyField('Tag', related_name="lessons",blank=True, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name