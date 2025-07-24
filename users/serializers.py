from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .validators import ComplexityValidator
from zxcvbn import zxcvbn

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password_strength = serializers.SerializerMethodField()

    def get_password_strength(self, obj):
        return zxcvbn(self.initial_data['password'])['score']
    
    class Meta:
        fields = [..., 'password_strength']

    password = serializers.CharField(
        write_only=True,
        validators=[
            validate_password,
            ComplexityValidator(min_score=3)
        ]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['useranme'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user