from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Course(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='course/%Y/%m/')
    Category = models.ForeignKey(Category,on_delete=models.PROTECT)

    def __str__(self):
        return self.name


# Create your models here.
