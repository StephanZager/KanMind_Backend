from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        return obj.owner == request.user
    
class IsMember(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        return request.user in obj.members.all()    