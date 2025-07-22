from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.owner == request.user


class IsMember(BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.user in obj.members.all()


class IsBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):

        return request.user in obj.board.members.all()


class CanUpdateOrDestroyTask(permissions.BasePermission):

    message = "Sie haben keine Berechtigung, diese Aktion auszuführen."

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'PATCH']:
            self.message = "Sie müssen Mitglied des Boards sein, um die Task zu sehen oder zu bearbeiten."
            return request.user in obj.board.members.all()

        if request.method == 'DELETE':
            self.message = "Nur der Eigentümer des Boards kann diese Task löschen."
            return obj.board.owner == request.user

        return False
