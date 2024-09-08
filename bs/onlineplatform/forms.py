from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Обязательное поле. Введите действующий адрес электронной почты.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применение классов Bootstrap ко всем полям
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control mb-3'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'photo', 'birth_date', 'phone_number', 'reader_ticket', 'favorite_categories']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Полное имя'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'reader_ticket': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Читательский билет'}),
            'favorite_categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применение классов Bootstrap ко всем полям
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control mb-3'})

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['full_name', 'subject', 'club', 'contact_method', 'contact_info', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше полное имя'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема'}),
            'club': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название клуба'}),
            'contact_method': forms.Select(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Контактная информация'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ваше сообщение'}),
        }

    def __init__(self, *args, **kwargs):
        show_club = kwargs.pop('show_club', False)
        super().__init__(*args, **kwargs)
        if not show_club:
            self.fields.pop('club')

        # Применение классов Bootstrap ко всем полям
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control mb-3'})

class BookSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        label='Название книги',
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Bootstrap класс для input
            'placeholder': 'Название книги'  # Добавить плейсхолдер
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Категория',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    author = forms.CharField(
        required=False,
        label='Авторы',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Авторы'
        })
    )
    publisher = forms.CharField(
        required=False,
        label='Издатель',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Издатель'
        })
    )
    language = forms.CharField(
        required=False,
        label='Язык',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Язык'
        })
    )
    format = forms.ChoiceField(
        choices=Book.FORMAT_CHOICES,
        required=False,
        label='Формат',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    publication_date_from = forms.DateField(
        required=False,
        label='Дата публикации от',
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    publication_date_to = forms.DateField(
        required=False,
        label='Дата публикации до',
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['feedback', 'value']
        widgets = {
            'value': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }

class AddToBookshelfForm(forms.ModelForm):
    class Meta:
        model = Bookshelf
        fields = ['private']  # Убедитесь, что поле private включено в форму

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['private'].widget = forms.RadioSelect(choices=[(True, 'Приватная'), (False, 'Публичная')])

class BookCrossingAdForm(forms.ModelForm):
    class Meta:
        model = BookCrossingAd
        fields = ['title', 'cover_image', 'short_description', 'detailed_description', 'contact_phone', 'contact_info']