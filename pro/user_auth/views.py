from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from . models import*
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser

from . serializers import UserSerializer
from rest_framework import status
from django.conf import settings
from rest_framework_jwt.serializers import jwt_payload_handler
import jwt
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import authenticate, login , logout
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

class CreateUserAPIView(APIView):
	permission_classes = (AllowAny,)
 
	def post(self, request):
		user = request.data
		serializer = UserSerializer(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)

 
class authenticate_user(APIView):
	permission_classes = ([AllowAny,]) 
	def post(self,request):
		try:
			email = request.data['email']
			password = request.data['password']
			user = authenticate(email=email, password=password) 
			if user:
				try:
					payload = jwt_payload_handler(user)
					token = jwt.encode(payload, settings.SECRET_KEY)
					login(request, user)
					user_details = {}
					user_details['name'] = "%s %s" % (user.first_name, user.last_name)
					user_details['token'] = token
					user_logged_in.send(sender=user.__class__,request=request, user=user)
					return Response(user_details, status=status.HTTP_200_OK)
	 
				except Exception as e:
					raise e
			else:
				res = {
					'error': 'can not authenticate with the given credentials or the account has been deactivated'}
				return Response(res, status=status.HTTP_403_FORBIDDEN)
		except KeyError:
			res = {'error': 'please provide a email and a password'}
			return Response(res)




# from django.utils import timezone
# from datetime import timedelta
# from datetime import datetime
# import pytz
# from pytz import utc
# class LoginView(APIView):
# 	def post(self,request):
# 		context = {}
# 		try:
# 			phone_number = request.data.get('phone_number')
# 			password = request.data.get('password')
# 			user = authenticate(phone_number=phone_number,password=password)
# 			if user:
# 				token,create = Token.objects.get_or_create(user=user)
			
# 				utc_now = datetime.utcnow()
# 				utc_now = utc_now.replace(tzinfo=pytz.utc)
# 				if token.created < utc_now - timedelta(seconds=10):
# 					token.delete()
# 					context['message'] = 'Invalid Token'
# 					return 	Response(context)
# 				else:
# 					token.created = datetime.utcnow()
# 					token.save()
# 				context['sucess'] = True
# 				if user.is_superuser or user.is_staff:
# 					context['is_superuser']= True
# 				else:
# 					context['is_superuser']= False
# 				context['message'] = 'User Login Successfully'
# 				context['data'] = { 'token': token.key }
# 				# context['user'] = {'username': username}
# 				login(request, user)
# 				return Response(context)
# 			else:
# 				context['success'] = False
# 				context['message'] = 'Invalid username or password'
# 				return Response(context)
# 		except Exception as e:
# 			context['success'] = False
# 			context['message'] = str(e)
# 			return Response(context)