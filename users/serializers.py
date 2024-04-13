from rest_framework import serializers
from .models import Doctor, Patient, CustomUser

class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user.name')
    class Meta:
        model = Doctor
        fields = ['id', 'specialization', 'availability', 'hospital', 'phone_number', 'user','name']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'gender', 'phone_number']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_staff', 'is_active', 'age', 'user_type', 'password','name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        #user = CustomUser.objects.create_user(password=password, **validated_data)
        return user
