from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound
from ..models import Board, Tasks, Comment


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsMember(BasePermission):
    """
    Object-level permission to only allow members of an object to access it.
    Assumes the model instance has a `members` many-to-many relationship.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsBoardMember(BasePermission):
    """
    Object-level permission to only allow members of an associated board.
    Assumes the model instance has a `board` foreign key attribute.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.board.members.all()


class CanUpdateOrDestroyTask(permissions.BasePermission):
    """
    Custom permission to control access to a single Task object.

    - Allows board members to view and update the task (GET, PUT, PATCH).
    - Allows the task creator or the board owner to delete the task (DELETE).
    """
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
    """
    View-level permission to check if a user can access a task's comments.

    Allows access only if the user is a member of the board to which the
    task belongs. Used for listing and creating comments where no comment
    object exists yet.
    """
    message = "You must be a member of the board to view or create comments."

    def has_permission(self, request, view):
        try:
            task = Tasks.objects.get(pk=view.kwargs['task_id'])
        except Tasks.DoesNotExist:
            raise NotFound("Task not found.")
        return request.user in task.board.members.all()


class IsCommentAuthor(BasePermission):
    """
    Object-level permission to only allow the author of a comment to delete it.
    Assumes the model instance has an `author` attribute.
    """
    message = "Only the creator of the comment is allowed to delete it."

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
