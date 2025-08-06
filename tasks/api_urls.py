from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='api-task')
router.register(r'categories', views.CategoryViewSet, basename='api-category')
router.register(r'comments', views.TaskCommentViewSet, basename='api-comment')

app_name = 'tasks-api'

urlpatterns = [
    path('', include(router.urls)),
] 