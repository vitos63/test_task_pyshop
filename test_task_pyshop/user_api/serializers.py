from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators = [UniqueValidator(queryset=User.objects.all(), message="The user's username already exists")])
    email = serializers.EmailField(validators = [UniqueValidator(queryset=User.objects.all(), message="The user's email address already exists")])
    password1 = serializers.CharField(write_only=True, min_length = 8, label = 'Password1')
    password2 = serializers.CharField(write_only=True, min_length = 8, label = 'Password2')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    

    def validate(self, attrs):
        if attrs['password1']!=attrs['password2']:
            raise serializers.ValidationError({'password2':"Passwords don't match"})
        
        return attrs
    

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
        )

        return user


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False, validators = [UniqueValidator(queryset=User.objects.all(), message="The user's username already exists")])
    email = serializers.EmailField(required=False, validators = [UniqueValidator(queryset=User.objects.all(), message="The user's email address already exists")])
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta():
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
    
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        return instance

        