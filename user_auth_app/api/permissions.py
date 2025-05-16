from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwner(permissions.BasePermission):
      
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user
    
    
class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.board.owner_id == user or user in obj.board.members.all()    