from rest_framework import permissions
from .models import UserBookAccess

class IsPurchased(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return UserBookAccess.objects.filter(user=request.user, book=obj.book).exists()