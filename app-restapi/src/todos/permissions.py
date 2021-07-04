from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    # TODO yetkisi olmayan user in erişimi kontrol ve kayıt işlemleri yapılabilir.
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
