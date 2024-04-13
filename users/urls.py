from django.urls import path
from .views import DoctorListCreateAPIView, PatientListCreateAPIView, DoctorAvailabilityAPIView, AvailableDoctorsAPIView
from .views import UserRegistrationAPIView, UserLoginAPIView

urlpatterns = [
    path('doctors/', DoctorListCreateAPIView.as_view(), name='doctor-list-create'),
    path('patients/', PatientListCreateAPIView.as_view(), name='patient-list-create'),
    path('api/doctors/<int:pk>/update_availability/', DoctorAvailabilityAPIView.as_view(), name='update_doctor_availability'),
    path('api/doctors/available/', AvailableDoctorsAPIView.as_view(), name='get_available_doctors'),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
]

