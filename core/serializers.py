from rest_framework import serializers
from django.db import models
from core.models import User, CheckoutInfo
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group


class ContactSerializer(serializers.Serializer):

    email = serializers.EmailField()
    subject = serializers.CharField()
    content = serializers.CharField()


class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenziali non corrette")


class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
            'profile_img',
            'user_type'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }
    
    def save(self):
        validated_data = self.validated_data
        
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        user = User.objects.create(**validated_data)

        if password != password2:
            return serializers.ValidationError({'password': 'Password must match'})
        user.set_password(password2)
        user.save()

        return user


class PostCheckoutInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckoutInfo
        fields = '__all__'


class CheckoutInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckoutInfo
        exclude = ('id', 'user', )
