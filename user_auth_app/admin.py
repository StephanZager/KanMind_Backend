from django.contrib import admin
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# UserProfile im Admin-Bereich registrieren
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_email')  
    search_fields = ('user__username', 'user__email') 

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'