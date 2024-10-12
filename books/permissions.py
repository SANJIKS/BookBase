from rest_framework import permissions
from .models import Purchase

class IsAuthenticatedAndPurchased(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return Purchase.objects.filter(user=request.user, book=obj.book).exists()