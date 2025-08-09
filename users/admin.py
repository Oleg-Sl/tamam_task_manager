from django.contrib import admin

from users.models import CustomUser, UserToken


admin.site.register(CustomUser)
admin.site.register(UserToken)
