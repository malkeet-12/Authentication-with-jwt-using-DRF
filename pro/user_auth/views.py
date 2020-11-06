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



class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)