from django.db import models
from authentication.models import CustomUser


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_projects')
    assigned_to = models.ManyToManyField(CustomUser, related_name='assigned_projects',
                                         limit_choices_to={'is_manager': True})
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ManyToManyField(CustomUser, related_name='assigned_tasks',
                                         limit_choices_to={'is_employee': True})
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks',
                                   limit_choices_to={'is_manager': True})
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(choices=((1, 'Low'), (2, 'Medium'), (3, 'High')), default=2)
    status = models.CharField(max_length=20,
                              choices=(('todo', 'To Do'), ('inprogress', 'In Progress'), ('done', 'Done')),
                              default='todo')
