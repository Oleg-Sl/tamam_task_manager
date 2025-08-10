from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('task-manager/admin/', admin.site.urls),
    path('task-manager/accounts/', include('django.contrib.auth.urls')),
    path('task-manager/tasks/', include('tasks.urls')),
]
