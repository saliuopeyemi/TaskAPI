from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
import uuid


status = (("Completed","Completed"),("Started","Started"),("Incomplete","Incomplete"))

class RegisterSerializer(serializers.Serializer):
	first_name = serializers.CharField(max_length=500, required=True)
	last_name = serializers.CharField(max_length=500,required=True)
	email = serializers.CharField(max_length=500,required=True)
	age= serializers.IntegerField()
	dob = serializers.DateField(format="%d-%m-%Y")
	password = serializers.CharField(max_length=500,required=True)

	def validate_email(self,value):
		if "@" not in value:
			raise serializers.ValidationError("Entry not an email!")
		else:
			return value

	def validate(self,data):
		email = data["email"]
		user = User.objects.filter(email=email)
		if user.exists():
			raise serializers.ValidationError("Existing Email!")
		else:
			return data

	def create(self,validated_data):
		username=uuid.uuid4()
		user_detail = User.objects.create(
		                                  email=validated_data["email"],
		                                  username=username,
		                                  password=validated_data["password"]
		                                  )
		new_user_id = User.objects.get(email=validated_data["email"]).id
		models.UserExtend.objects.create(
		                                 id_id=new_user_id,
		                                 first_name=validated_data["first_name"],
		                                 last_name=validated_data["last_name"],
		                                 dob = validated_data["dob"],
		                                 age = validated_data["age"]
		                                 )
		return user_detail

class LoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=200)
	password = serializers.CharField(max_length=200)

	def validate(self,data):
		user = User.objects.filter(email=data["email"]).first()
		if user and (user.password == data["password"]):
			return user
		else:
			raise serializers.ValidationError("Invalid Credentials")

class TaskSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=300,required=True)
	description = serializers.CharField(max_length=9999999,required=True)

	def validate(self,data):
		request = self.context["request"]
		user_id = request.user
		data["id"] = user_id
		return data

	def create(self,validated_data):
		new_task = models.Tasks.objects.create(
		                                      owner_id=validated_data["id"],
		                                      name = validated_data["name"],
		                                      description = validated_data["description"]
		                                      )
		return new_task

class TaskUpdateSerializer(serializers.Serializer):
	task_id = serializers.IntegerField()
	description = serializers.CharField(max_length=99999999,required=False)
	status = serializers.ChoiceField(choices=status,required=False)

	def validate(self,data):
		request = self.context["request"]
		task = models.Tasks.objects.filter(id=data["task_id"],owner_id=request.user.id)
		# if request.user.id != task.first().owner_id:
		# 	raise serializers.ValidationError("Ownership Error")
		if len(task) == 0:
			raise serializers.ValidationError("Invalid Task ID")
		else:
			task = task.first()
			status = task.status
			if status == "Completed":
				raise serializers.ValidationError("Task Already Completed")
			elif status == "Started" and (data["status"] == "Incomplete"):
				raise serializers.ValidationError("Cannot revert status")
			else:
				return data

	def create(self,validated_data):
		task = models.Tasks.objects.filter(id=validated_data["task_id"])
		try:
			validated_data["description"]
			try:
				validated_data["status"]
			except:
				validated_data["status"] = None
		except:
			validated_data["description"] = None
		if validated_data["description"] != None and validated_data["status"] != None:
			task.update(description=validated_data["description"],status=validated_data["status"])
		elif validated_data["description"] == None and validated_data["status"] != None:
			task.update(status=validated_data["status"])
		elif validated_data["description"] != None and validated_data["status"] == None:
			task.update(description=validated_data["description"])

		output_data = {"status":"Success","Description":validated_data["description"],"Status":validated_data["status"]}
		return output_data

class TaskDeleteSerializer(serializers.Serializer):
	task_id = serializers.IntegerField()

	def validate(self,data):
		request= self.context["request"]
		try:
			task = models.Tasks.objects.get(id=data["task_id"],owner_id=request.user.id)
		except:
			raise serializers.ValidationError("Inexistent Task")
		task.delete()
		return data