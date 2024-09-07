from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Переход на страницу после успешной регистрации
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def index(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = FeedbackForm(request.POST, show_club=False)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.save()
            return redirect('index')
    else:
        form = FeedbackForm(show_club=False)
    context = {'categories': categories, 'form': form}
    return render(request, 'index.html', context)

def book_list(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        if form.cleaned_data['title']:
            books = books.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['author']:
            books = books.filter(author=form.cleaned_data['author'])
        if form.cleaned_data['publisher']:
            books = books.filter(publisher__icontains=form.cleaned_data['publisher'])
        if form.cleaned_data['language']:
            books = books.filter(language__icontains=form.cleaned_data['language'])
        if form.cleaned_data['format']:
            books = books.filter(format=form.cleaned_data['format'])
        if form.cleaned_data['publication_date_from']:
            books = books.filter(publication_date__gte=form.cleaned_data['publication_date_from'])
        if form.cleaned_data['publication_date_to']:
            books = books.filter(publication_date__lte=form.cleaned_data['publication_date_to'])
    
    context = {
        'form': form,
        'books': books
    }
    return render(request, 'catalog.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = Review.objects.filter(subject=book)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if request.user.is_authenticated:
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.subject = book
                review.user = request.user
                review.save()
                return redirect('book_detail', pk=book.pk)
        else:
            return redirect('login')  # Переадресация на страницу авторизации, если пользователь не аутентифицирован
    else:
        review_form = ReviewForm()
    
    context = {
        'book': book,
        'reviews': reviews,
        'review_form': review_form
    }
    return render(request, 'book_detail.html', context)

def cabinet(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'cabinet.html', context)

