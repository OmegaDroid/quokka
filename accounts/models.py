from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User)

    firstName = models.CharField(max_length=100, null=False)
    lastName = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)

    @property
    def name(self):
        return self.firstName+" "+self.lastName

    def __str__(self):
        return self.name

