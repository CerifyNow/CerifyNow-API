from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    InstitutionReadAPIView,
    CertificateReadAPIView,
    InstitutionCreateAPIView,
    CertificateCreateAPIView,
    CertificateDetailAPIView,
)

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('institutions/', InstitutionReadAPIView.as_view(), name='institution-read'),
    path('institutions/create', InstitutionCreateAPIView.as_view(), name='institution-create'),
    path('certificates/', CertificateReadAPIView.as_view(), name='certificate-read'),
    path('certificates/create', CertificateCreateAPIView.as_view(), name='certificate-create'),
    path('certificates/<uuid:pk>/', CertificateDetailAPIView.as_view(), name='certificate-detail')
]
