from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'profile_photo']

        def create(self, validated_data):
            role = validated_data.get("role")
            if role == "superadmin":
                validated_data["is_staff"] = True
                validated_data["is_superuser"] = True
            else:
                validated_data["is_staff"] = False
                validated_data["is_superuser"] = False
            return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
