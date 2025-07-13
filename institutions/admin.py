from django.contrib import admin
from django.utils.html import format_html

from .models import Institution, Certificate

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'is_approved', 'institution_logo', 'institution_seal')
    search_fields = ('name', )
    list_filter = ('is_approved', 'created_at')
    ordering = ('-created_at',)

    def institution_logo(self, obj):
        return format_html(f'''<a href="{obj.logo.url}" target="_blank"><img src="{obj.logo.url}"
            alt="image" width="100 height="100" style="object-fit : cover;"/></a>''')

    def institution_seal(self, obj):
        return format_html(f'''<a href="{obj.seal.url}" target="_blank"><img src="{obj.seal.url}"
            alt="image" width="100 height="100" style="object-fit : cover;"/></a>''')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'student__full_name', 'institution', 'issued_date', 'is_verified', 'certificate_file', 'certificate_qr_code')
    search_fields = ('serial_number', 'student__full_name', 'institution__name')
    list_filter = ('is_verified', 'institution', 'issued_date')
    ordering = ('-issued_date',)

    def certificate_file(self, obj):
        return format_html(f'''<a href="{obj.file.url}" target="_blank"><img src="{obj.file.url}"
            alt="image" width="100 height="100" style="object-fit : cover;"/></a>''')

    def certificate_qr_code(self, obj):
        return format_html(f'''<a href="{obj.qr_code.url}" target="_blank"><img src="{obj.qr_code.url}"
                    alt="image" width="100 height="100" style="object-fit : cover;"/></a>''')
