from django.contrib import admin

from django.contrib.auth import get_user_model
UserModel = get_user_model()

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    model = UserModel
    list_display = 'full_name', 'email', 'username', 'is_superuser'
    list_display_links = 'full_name', 'email'