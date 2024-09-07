from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Обязательное поле. Введите действующий адрес электронной почты.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['full_name', 'subject', 'club', 'contact_method', 'contact_info', 'message']
    
    def __init__(self, *args, **kwargs):
        show_club = kwargs.pop('show_club', False)
        super().__init__(*args, **kwargs)
        if not show_club:
            self.fields.pop('club')


class BookSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Название книги')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Категория')
    author = forms.CharField(required=False, label='Авторы')
    publisher = forms.CharField(required=False, label='Издатель')
    language = forms.CharField(required=False, label='Язык')
    format = forms.ChoiceField(choices=Book.FORMAT_CHOICES, required=False, label='Формат')
    publication_date_from = forms.DateField(required=False, label='Дата публикации от', widget=forms.TextInput(attrs={'type': 'date'}))
    publication_date_to = forms.DateField(required=False, label='Дата публикации до', widget=forms.TextInput(attrs={'type': 'date'}))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['feedback', 'value']
        widgets = {
            'value': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }