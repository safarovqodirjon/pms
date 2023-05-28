from django import forms
from .models import ProjectCompletionRequest, Project, TaskCompletionRequest, Task
from authentication.models import CustomUser
from django.forms import DateInput


class DatePickerInput(DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, format=None):
        if attrs is None:
            attrs = {}
        attrs['lang'] = 'ru'
        super().__init__(attrs, format)


class ProjectForm(forms.ModelForm):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control col-12'}))
    description = forms.CharField(label='Описание',
                                  widget=forms.Textarea(attrs={'class': 'form-control form-control-lg'}))
    created_by = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_superuser=True),
                                        widget=forms.Select(attrs={'class': 'custom-select col-12'}),
                                        label='Для админа',
                                        empty_label=None)
    start_date = forms.DateField(
        widget=DatePickerInput(attrs={'class': 'form-control'}),
        label='Начало'
    )
    end_date = forms.DateField(
        widget=DatePickerInput(attrs={'class': 'form-control'}),
        label='Дэдлайн'
    )
    project_status = forms.ChoiceField(choices=(
        ('not_started', 'Не начат'), ('in_progress', 'В процессе'), ('completed', 'Завершен')),
        widget=forms.Select(attrs={'class': 'custom-select col-12'}), label='Статус проекта'
    )
    image = forms.ImageField(label='Изображение')

    class Meta:
        model = Project
        fields = ['name', 'description', 'created_by', 'start_date', 'end_date', 'project_status', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].empty_label = None
        if self.fields['created_by'].queryset.exists():
            self.fields['created_by'].initial = self.fields['created_by'].queryset.first()

        # self.fields['assigned_to'].queryset = CustomUser.objects.filter(is_manager=True)


class TaskForm(forms.ModelForm):
    name = forms.CharField(label='Задача', widget=forms.TextInput(attrs={'class': 'form-control col-12'}))
    project = forms.ModelChoiceField(queryset=Project.objects.none(), empty_label='Выберете проект',
                                     widget=forms.Select(attrs={'class': 'custom-select col-12'}), label='Проект')
    assigned_to = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(is_employee=True),
                                                 widget=forms.SelectMultiple(attrs={'class': 'custom-select col-12'}),
                                                 label='Назначено', to_field_name="username")
    due_date = forms.DateField(
        widget=DatePickerInput(attrs={'class': 'form-control'}),
        label='Срок выполнения'
    )
    priority = forms.ChoiceField(choices=((1, 'Легко'), (2, 'Среднее'), (3, 'Сложно')),
                                 widget=forms.Select(attrs={'class': 'custom-select col-12'}), label='Приоритет')
    status = forms.ChoiceField(choices=(('todo', 'Не начать'), ('inprogress', 'В прогрессе'), ('done', 'Закончено')),
                               widget=forms.Select(attrs={'class': 'custom-select col-12'}), label='Статус')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-lg'}),
                                  label='Описание', required=False)

    class Meta:
        model = Task
        fields = ['name', 'description', 'project', 'assigned_to', 'due_date', 'priority', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(assigned_to=user)
            self.fields['assigned_to'].label_from_instance = lambda obj: f"{obj.last_name} {obj.first_name}"


class ProjectCompletionRequestForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label='Выберете проект',
                                     widget=forms.Select(attrs={'class': 'custom-select col-12'}))
    user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_manager=True), empty_label='Выберете менеджера',
                                  widget=forms.Select(attrs={'class': 'custom-select col-12'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-lg'}),
                                  label='Описание', required=False)

    class Meta:
        model = ProjectCompletionRequest
        fields = ['project', 'user', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['user'].widget.attrs.update({'class': 'form-control form-control-lg'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.cleaned_data['user']
        instance.description = self.cleaned_data['description']
        if commit:
            instance.save()
        return instance


class TaskCompletionRequestForm(forms.ModelForm):
    task = forms.ModelChoiceField(queryset=Task.objects.all(), empty_label='Выберите задачу',
                                  widget=forms.Select(attrs={'class': 'custom-select col-12'}))
    user = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_employee=True),
                                  empty_label='Выберите сотрудника',
                                  widget=forms.Select(attrs={'class': 'custom-select col-12'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = TaskCompletionRequest
        fields = ['task', 'user', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['user'].widget.attrs.update({'class': 'form-control form-control-lg'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.cleaned_data['user']
        if commit:
            instance.save()
        return instance
