from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import AdvUser,UserIp


class AdvUserIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIp
        fields = ('ip','user','count_post','count_get')


class AdvUserSerializer(serializers.ModelSerializer):
    absuser = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AdvUser
        fields = ('id','username','first_name','last_name','absuser')


class RegisterUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=16,min_length=7,write_only=True)

    token=serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model = AdvUser
        fields = ('email','username','password','token')

    def create(self, validated_data):
        return AdvUser.objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    email=serializers.EmailField(write_only=True)
    password=serializers.CharField(max_length=128,write_only=True)

    username=serializers.CharField(max_length=255,read_only=True)
    token=serializers.CharField(max_length=255,read_only=True)

    def validate(self,data):
        email=data.get('email',None)
        password=data.get('password',None)

        if email is None:
            raise serializers.ValidationError('Email not for user')

        if password is None:
            raise serializers.ValidationError('Password not for user')

        user=authenticate(username=email,password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password not found')

        if not user.is_active:
            raise serializers.ValidationError('A User was deactivated')

        return {
            'token':user.token
        }

