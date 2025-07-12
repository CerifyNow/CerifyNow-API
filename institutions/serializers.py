from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Institution, Certificate


class InstitutionSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)

    class Meta:
        model = Institution
        fields = [
            'id', 'name', 'inn', 'address', 'phone', 'email', 'seal',
            'logo', 'website', 'is_approved', 'admin', 'created_at'
        ]


class CertificateSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = [
            'id', 'institution', 'student', 'file',
            'document_type', 'issued_date', 'description', 'qr_code_url'
        ]
        read_only_fields = ['hash', 'qr_code']

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code:
            url = obj.qr_code.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None

