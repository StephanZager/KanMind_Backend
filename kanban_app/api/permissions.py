from rest_framework import permissions
from rest_framework.permissions import BasePermission
from ..models import Board, Tasks, Comment


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

    message = "You do not have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'PATCH']:
            self.message = "You must be a member of the board to view or edit the task."
            return request.user in obj.board.members.all()

        if request.method == 'DELETE':
            self.message = "Only the task creator or board owner can delete it."
            is_creator = obj.creator == request.user
            is_board_owner = obj.board.owner == request.user
            return is_creator or is_board_owner

        return False


class CanAccessTaskComments(BasePermission):
    message = "You must be a member of the board to view or create comments. "

    def has_permission(self, request, view):
        try:
            task = Tasks.objects.get(pk=view.kwargs['task_id'])
            return request.user in task.board.members.all()
        except Tasks.DoesNotExist:
            return False


class IsCommentAuthor(BasePermission):
    message = "Only the creator of the comment is allowed to delete it."

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
