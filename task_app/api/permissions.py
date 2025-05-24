from rest_framework.permissions import BasePermission

class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        task_id = view.kwargs.get('task_id')
        from task_app.models import Tasks
        try:
            task = Tasks.objects.get(id=task_id)
        except Tasks.DoesNotExist:
            return False
        return request.user in task.board.members.all() or task.board.owner == request.user

class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user