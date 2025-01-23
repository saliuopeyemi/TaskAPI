from django.db import models
from django.contrib.auth.models import User


class UserExtend(models.Model):
	id = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	first_name = models.CharField(max_length=500)
	last_name = models.CharField(max_length=500)
	dob = models.CharField(max_length=150)
	age = models.IntegerField()

class Tasks(models.Model):
	owner_id = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=300)
	description = models.TextField()
	status = models.CharField(max_length=50,default="Incomplete")
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)