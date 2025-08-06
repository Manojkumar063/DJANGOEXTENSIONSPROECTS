from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Category, TaskComment
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'description', 'created_at']


class TaskCommentSerializer(serializers.ModelSerializer):
    """Serializer for TaskComment model"""
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)
    is_overdue = serializers.ReadOnlyField()
    priority_color = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'created_by', 'assigned_to', 
            'category', 'priority', 'status', 'due_date', 'created_at', 
            'updated_at', 'completed_at', 'is_overdue', 'priority_color',
            'comments'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'completed_at']


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks"""
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'category', 'priority', 'status', 'due_date']
    
    def validate_due_date(self, value):
        """Validate that due date is not in the past"""
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tasks"""
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'category', 'priority', 'status', 'due_date']
    
    def validate_due_date(self, value):
        """Validate that due date is not in the past"""
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value 