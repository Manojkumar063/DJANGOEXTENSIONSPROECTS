from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Category, TaskComment
from .forms import TaskForm, CategoryForm, TaskCommentForm, TaskFilterForm
from .serializers import TaskSerializer, CategorySerializer, TaskCommentSerializer


# Dashboard View
@login_required
def dashboard(request):
    """Dashboard view showing task overview and statistics"""
    user = request.user
    
    # Get task statistics
    total_tasks = Task.objects.filter(
        Q(created_by=user) | Q(assigned_to=user)
    ).count()
    
    tasks_by_status = Task.objects.filter(
        Q(created_by=user) | Q(assigned_to=user)
    ).values('status').annotate(count=Count('status'))
    
    overdue_tasks = Task.objects.filter(
        Q(created_by=user) | Q(assigned_to=user),
        due_date__lt=timezone.now(),
        status__in=['todo', 'in_progress', 'review']
    ).count()
    
    recent_tasks = Task.objects.filter(
        Q(created_by=user) | Q(assigned_to=user)
    ).order_by('-created_at')[:5]
    
    context = {
        'total_tasks': total_tasks,
        'tasks_by_status': tasks_by_status,
        'overdue_tasks': overdue_tasks,
        'recent_tasks': recent_tasks,
    }
    return render(request, 'tasks/dashboard.html', context)


# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    """List view for tasks with filtering and search"""
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Task.objects.filter(
            Q(created_by=self.request.user) | Q(assigned_to=self.request.user)
        )
        
        # Apply filters
        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('search'):
                search = form.cleaned_data['search']
                queryset = queryset.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )
            
            if form.cleaned_data.get('status'):
                queryset = queryset.filter(status=form.cleaned_data['status'])
            
            if form.cleaned_data.get('priority'):
                queryset = queryset.filter(priority=form.cleaned_data['priority'])
            
            if form.cleaned_data.get('category'):
                queryset = queryset.filter(category=form.cleaned_data['category'])
            
            if form.cleaned_data.get('assigned_to'):
                queryset = queryset.filter(assigned_to=form.cleaned_data['assigned_to'])
            
            if form.cleaned_data.get('due_date_from'):
                queryset = queryset.filter(due_date__gte=form.cleaned_data['due_date_from'])
            
            if form.cleaned_data.get('due_date_to'):
                queryset = queryset.filter(due_date__lte=form.cleaned_data['due_date_to'])
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    """Detail view for individual tasks"""
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    
    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) | Q(assigned_to=self.request.user)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = TaskCommentForm()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Create view for new tasks"""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update view for editing tasks"""
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    
    def test_func(self):
        task = self.get_object()
        return task.created_by == self.request.user or task.assigned_to == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete view for removing tasks"""
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
    def test_func(self):
        task = self.get_object()
        return task.created_by == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    """List view for categories"""
    model = Category
    template_name = 'tasks/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20


class CategoryDetailView(LoginRequiredMixin, DetailView):
    """Detail view for categories with related tasks"""
    model = Category
    template_name = 'tasks/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(
            category=self.object
        ).filter(
            Q(created_by=self.request.user) | Q(assigned_to=self.request.user)
        ).order_by('-created_at')
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Create view for new categories"""
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for editing categories"""
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for removing categories"""
    model = Category
    template_name = 'tasks/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Comment Views
@login_required
def add_comment(request, task_id):
    """Add a comment to a task"""
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('task_detail', pk=task_id)


@login_required
def delete_comment(request, comment_id):
    """Delete a comment"""
    comment = get_object_or_404(TaskComment, id=comment_id)
    
    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
    else:
        messages.error(request, 'You cannot delete this comment.')
    
    return redirect('task_detail', pk=comment.task.id)


# AJAX Views
@login_required
def mark_task_complete(request, task_id):
    """Mark a task as complete via AJAX"""
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        if task.created_by == request.user or task.assigned_to == request.user:
            task.mark_completed()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


# API Viewsets
class TaskViewSet(viewsets.ModelViewSet):
    """API viewset for tasks"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) | Q(assigned_to=self.request.user)
        )
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.mark_completed()
        return Response({'status': 'success'})


class CategoryViewSet(viewsets.ModelViewSet):
    """API viewset for categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskCommentViewSet(viewsets.ModelViewSet):
    """API viewset for task comments"""
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return (TaskComment.objects.filter(
            task__created_by=self.request.user
        ) | TaskComment.objects.filter(
            task__assigned_to=self.request.user
        ))
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 