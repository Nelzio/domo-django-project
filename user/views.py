# from django.shortcuts import render
from django.http import Http404
import random
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from pprint import pprint
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
# from .forms import RegisterForm, UserAdminCreationForm
# from django.contrib.auth import authenticate, login, logout


from .models import User, Code
from .serializers import UserSerializer, CodeSerializer

def generate_auth_code():
    """Generate a random code """
    code_list = [random.randint(0, 9) for i in range(6)]
    code = ""
    for item in code_list:
        code += str(item)
    return int(code)

class UserView(APIView):
    """
    View to create new user
    """
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetails(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        data = request.data
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes((AllowAny,))
def reset_pass_code_api(request, format=None):
    data = request.data
    try:
        user = User.objects.get(email=data["email"])
    except Code.DoesNotExist:
        Response(status=status.HTTP_404_NOT_FOUND)
    data["user"] = user.id
    data["code"] = generate_auth_code()

    try:
        code = Code.objects.get(user=user)
        serializer = CodeSerializer(code, data=data)
    except Code.DoesNotExist:
        serializer = CodeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def reset_pass_api(request, format=None):
    data = request.data
    try:
        code = Code.objects.get(code=data["code"])
    except Code.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        user = User.objects.get(id=code.user.id)
        user.set_password(data["password"])
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)