from rest_framework.permissions import BasePermission, SAFE_METHODS

class CertificatePermissions(BasePermission):
    """
    - superadmin: barcha action (GET, POST, PUT, DELETE ...)
    - institutions: faqat Certificate create (POST)
    - student: faqat readonly (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # superadmin: barcha method ruxsat
        if user.role == 'superadmin':
            return True

        # institutions: faqat Certificate POST
        if user.role == 'institution_admin':
            return request.method == 'POST'

        # student: faqat readonly
        if user.role == 'student':
            return request.method in SAFE_METHODS

        return False


class InstitutionPermissions(BasePermission):
    """
    - superadmin: barcha action
    - institutions: hech narsa qila olmaydi
    - student: faqat readonly (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # superadmin: barcha method ruxsat
        if user.role == 'superadmin':
            return True

        # institutions: umuman ruxsat yo'q!
        if user.role == 'institutions':
            return False

        # student: faqat readonly
        if user.role == 'student':
            return request.method in SAFE_METHODS

        return False
