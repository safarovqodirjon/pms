from django.db import models
from authentication.models import CustomUser
from django.contrib.auth import get_user_model


class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_projects',
                                   verbose_name='Создано')
    assigned_to = models.ManyToManyField(CustomUser, related_name='assigned_projects',
                                         limit_choices_to={'is_manager': True}, blank=True, null=True,
                                         verbose_name='Назначено')
    start_date = models.DateField(null=True, blank=True, verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')
    project_status = models.CharField(max_length=20, choices=(
        ('not_started', 'Не начат'), ('in_progress', 'В процессе'), ('completed', 'Завершен')), default='not_started',
                                      verbose_name='Статус проекта')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    image = models.ImageField(upload_to="projects/%Y/%m/%d", blank=True, null=True, verbose_name='Изображение')
    approved_by_admin = models.BooleanField(default=False, verbose_name='Одобрено администратором')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name='Проект')
    assigned_to = models.ManyToManyField(CustomUser, related_name='assigned_tasks',
                                         limit_choices_to={'is_employee': True}, verbose_name='Назначено')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks',
                                   limit_choices_to={'is_manager': True}, verbose_name='Создано')
    due_date = models.DateField(null=True, blank=True, verbose_name='Срок выполнения')
    priority = models.IntegerField(choices=((1, 'Low'), (2, 'Medium'), (3, 'High')), default=2,
                                   verbose_name='Приоритет')
    status = models.CharField(max_length=20,
                              choices=(('todo', 'To Do'), ('inprogress', 'In Progress'), ('done', 'Done')),
                              default='todo', verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


# CustomUser = get_user_model()


class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    projects = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проекты')
    employees = models.ManyToManyField(CustomUser, related_name='managers', blank=True, verbose_name='Сотрудники')

    def __str__(self):
        return self.user.username


class ProjectCompletionRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='completion_requests',
                                verbose_name='Проект')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    request_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрено')
    description = models.TextField(verbose_name='Описание', blank=True)
    rating = models.IntegerField(verbose_name='Оценка', null=True, blank=True)

    class Meta:
        verbose_name = 'Запрос о завершении проекта'
        verbose_name_plural = 'Запросы о завершении проектов'

    def __str__(self):
        return f'{self.project} - {self.user}'

    def approve(self):
        self.is_approved = True
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_approved and self.rating is not None:
            self.user.rate = self.rating
            self.project.rating = (self.project.rating * self.project.rating_count + self.rating) / (
                    self.project.rating_count + 1)
            self.project.rating_count += 1

            self.user.save()
            self.project.save()


class TaskCompletionRequest(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='completion_requests',
                             verbose_name='Задача')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    request_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрено')
    description = models.TextField(verbose_name='Описание', null=True)

    class Meta:
        verbose_name = 'Запрос о завершении задачи'
        verbose_name_plural = 'Запросы о завершении задач'

    def __str__(self):
        return f'{self.task} - {self.user}'

    def approve(self):
        self.is_approved = True
        self.save()



