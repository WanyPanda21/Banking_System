from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "role",
            "address",
            "date_of_birth",
        ]

    def create(self, validated_data):  #validated_data contains only clean, validated values.
        password = validated_data.pop("password")  #we'll handle the password separately.

        user = User(**validated_data)     #create a user and It is not yet saved in the database.
        user.set_password(password)   # Encrypt password
        user.save()                   # stores everything in the database.

        return user                   #returns the newly created user object. now Control goes back to views.py