from rest_framework import serializers
from .models import CustomUser , Category , Product
import re   


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email","password" , "role"]
        
        extra_kwargs = {
            "password":{"write_only":True},
        
        }


    def create(self,validated_data):

        user = CustomUser.objects.create_user(**validated_data)

        return user



class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)



class OtpSerializer(serializers.Serializer):

    otp = serializers.CharField(required=True,max_length=6)



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"














