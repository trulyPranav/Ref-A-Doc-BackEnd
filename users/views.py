from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Doctor, Patient, CustomUser
from .serializers import DoctorSerializer, PatientSerializer, UserSerializer
import logging
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from django.contrib.auth import get_user_model

class DoctorListCreateAPIView(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Validate incoming data
        doctor_serializer = DoctorSerializer(data=request.data)
        if doctor_serializer.is_valid():
            # Extract user data and validate it
            user_data = request.data.pop('user')
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                # Create a new CustomUser instance
                user = user_serializer.save(user_type='doctor')
                
                # Create a new Doctor instance and associate it with the user
                doctor = doctor_serializer.save(user=user)
                return Response(doctor_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientListCreateAPIView(APIView):
    def post(self, request):
        user = request.user  # Assuming the user making the request is associated with the patient
        patient_data = {**request.data, 'user': user.id}  # Provide the 'user' field explicitly
        serializer = PatientSerializer(data=patient_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DoctorAvailabilityAPIView(APIView):
    def post(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response({"message": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        availability = request.data.get('availability')
        if availability is None:
            return Response({"message": "Availability is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        doctor.availability = availability
        doctor.save()
        return Response({"message": "Doctor availability updated successfully"}, status=status.HTTP_200_OK)

class AvailableDoctorsAPIView(APIView):
    def get(self, request):
        available_doctors = Doctor.objects.filter(availability=True)
        serialized_data = []
        for doctor in available_doctors:
            serialized_data.append({
                'id': doctor.id,
                'name': doctor.user.name,
                'specialization': doctor.specialization,
            })
        return Response(serialized_data, status=status.HTTP_200_OK)

class UserRegistrationAPIView(APIView):
    def post(self, request):
        # Validate incoming data using the UserSerializer
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            # Create a new CustomUser instance
            user = user_serializer.save()
            
            # Determine the user type and create the appropriate instance
            user_type = request.data.get('user_type')
            if user_type == 'doctor':
                # Create a new Doctor instance and associate it with the user
                doctor_data = request.data.get('doctor_data', {})
                Doctor.objects.create(user=user, **doctor_data)
            elif user_type == 'patient':
                # Create a new Patient instance and associate it with the user
                patient_data = request.data.get('patient_data', {})
                Patient.objects.create(user=user, **patient_data)
            
            # Return the serialized data
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        
        # Return any validation errors
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


logger = logging.getLogger(__name__)

class UserLoginAPIView(APIView):
    def post(self, request):
        # Extract email and password from the request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Retrieve the user based on email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # If user with the given email does not exist, return an error
            logger.warning(f"Invalid login attempt: User with email {email} not found")
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check the provided password against the stored hashed password
        if user.check_password(password):
            # Password is correct
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        else:
            # Password is incorrect
            logger.warning(f"Invalid login attempt: Incorrect password for email {email}")
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)