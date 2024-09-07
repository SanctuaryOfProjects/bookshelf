from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseRedirect

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
        if form.cleaned_data['category']:
            books = books.filter(category=form.cleaned_data['category'])
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

    book_forms = {}
    for book in books:
        book_forms[book.id] = AddToBookshelfForm()

    context = {
        'form': form,
        'books': books,
        'book_forms': book_forms
    }
    return render(request, 'catalog.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = Review.objects.filter(subject=book)
    
    if request.method == 'POST':
        if 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.subject = book
                review.user = request.user
                review.save()
                return redirect('book_detail', pk=book.pk)
        elif 'add_to_bookshelf_submit' in request.POST:
            add_to_bookshelf_form = AddToBookshelfForm(request.POST)
            if add_to_bookshelf_form.is_valid():
                if not Bookshelf.objects.filter(user=request.user, subject=book).exists():
                    bookshelf = add_to_bookshelf_form.save(commit=False)
                    bookshelf.user = request.user
                    bookshelf.subject = book
                    bookshelf.save()
                    return redirect('book_detail', pk=book.pk)
                else:
                    add_to_bookshelf_form.add_error(None, "Эта книга уже добавлена на вашу книжную полку.")
    else:
        review_form = ReviewForm()
        add_to_bookshelf_form = AddToBookshelfForm()
    
    context = {
        'book': book,
        'reviews': reviews,
        'review_form': review_form,
        'add_to_bookshelf_form': add_to_bookshelf_form
    }
    return render(request, 'book_detail.html', context)

@login_required
def cabinet(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('cabinet')
    else:
        form = UserProfileForm(instance=user_profile)
        
    context = {'user_profile': user_profile, 'form': form}
    return render(request, 'cabinet.html', context)

@login_required
def edit_profile(request):
    categories = Category.objects.all()
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('cabinet')
    else:
        form = UserProfileForm(instance=user_profile)
    context = {'form': form}
    return render(request, 'edit_profile.html', context)

@login_required
def add_to_bookshelf(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = AddToBookshelfForm(request.POST)
        if form.is_valid():
            bookshelf = form.save(commit=False)
            bookshelf.user = request.user
            bookshelf.subject = book
            bookshelf.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return redirect('book_detail', book_id=book_id)

@login_required
def bookshelf(request):
    bookshelves = Bookshelf.objects.filter(user=request.user)
    unique_books = {}
    for bookshelf in bookshelves:
        if bookshelf.subject_id not in unique_books:
            unique_books[bookshelf.subject_id] = bookshelf
    context = {
        'bookshelves': unique_books.values()
    }
    return render(request, 'bookshelf.html', context)


