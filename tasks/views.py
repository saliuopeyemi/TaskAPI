from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import serializers
from . import models
import re
from rest_framework_simplejwt.tokens import RefreshToken

Filter_keywords=["started","incomplete","completed"]
class test(APIView):
	def get(self,request):
		return Response("Hello world",status=status.HTTP_200_OK)

class RegisterView(APIView):
	permission_classes=[AllowAny,]
	serializer_class = serializers.RegisterSerializer

	def post(self,request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.save()
			output ={
				"status":"success",
				"email":user.email,
				}
			return Response(output,status=status.HTTP_201_CREATED)
		else:
			return Response(serializers.errors)


class LoginView(APIView):
	permission_classes = [
		AllowAny,
	]
	serializer_class = serializers.LoginSerializer

	def post(self,request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		refresh = RefreshToken.for_user(user)

		return Response({
		                	"Access":str(refresh.access_token),
		                	"Refresh": str(refresh)
		                }, status=status.HTTP_200_OK
		                )
		
class TaskView(APIView):
	permission_classes=[
		IsAuthenticated,
	]
	serializer_class = serializers.TaskSerializer

	def post(self,request):
		serializer = self.serializer_class(data=request.data,context={"request":request})
		serializer.is_valid(raise_exception=True)
		task = serializer.save()
		return Response({
		                "Detail":"Created",
		                "Task Name":task.name,
		                "Task Description":task.description
		                },status=status.HTTP_201_CREATED)

	def get(self,request):
		user_id = request.user.id
		all_tasks = models.Tasks.objects.filter(owner_id=user_id)
		container = []
		for task in all_tasks:
			item = {
				"Task ID":task.id,
				"Name":task.name,
				"Description":task.description,
				"Status":task.status,
				"Added":task.added,
				"Last Updated":task.updated
			}
			container.append(item)
		return Response({"Tasks":container},status=status.HTTP_200_OK)

class TaskUpdate(APIView):
	serializer_class=serializers.TaskUpdateSerializer
	permission_classes= [
		IsAuthenticated,
	]
	def post(self,request):
		serializer = self.serializer_class(data=request.data,context={"request":request})
		if serializer.is_valid(raise_exception=True):
			output = serializer.save()
			return Response(output,status=status.HTTP_201_CREATED)

	def delete(self,request):
		serializer = serializers.TaskDeleteSerializer(data=request.data,context={"request":request})
		serializer.is_valid(raise_exception=True)
		return Response({"Detail":"Task Deleted"},status=status.HTTP_204_NO_CONTENT)

class TaskFilter(APIView):
	permission_classes=[IsAuthenticated,]
	def get(self,request,keyword):
		if keyword.lower() not in Filter_keywords:
			return Response({"Error":"Invalid Filter"},status=status.HTTP_404_NOT_FOUND)
		else:
			user_id = request.user.id
			filter_results = models.Tasks.objects.filter(status=keyword.capitalize(),owner_id=user_id)
			container = []
			for result in filter_results:
				item = {
					"Id":result.id,
					"Title":result.name,
					"Description":result.description,
					"Status":result.status,
					"Added":result.added,
					"Last Updated":result.updated
				}
				container.append(item)
			return Response(container,status=status.HTTP_200_OK)

