from main.models import MyUser
from rest_framework import serializers

class ResgisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'gender', 'language', 'age']
    def validate(self, attrs):
        errors = dict()
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)
    
    def validate_username(self, value):
        if MyUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(f"Username {value} is already taken!")
        return value
    def validate_email(self, value):
        normalized_email = value.lower()  # Normalize email to lower case
        if MyUser.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError(f"Email address {normalized_email} is already taken!")
        return normalized_email
