from rest_framework import serializers
from .models import User, Code
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_user_name', 'telephone',
                  'last_user_name', 'id', 'staff', 'active', 'store_staff', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CodeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Code
        fields = '__all__'
