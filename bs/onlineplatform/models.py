from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


#Клубы

class Club(models.Model):
    name = models.CharField("Название клуба", max_length=255)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="led_clubs")
    preview_image = models.ImageField("Превью", upload_to="club_previews/", blank=True, null=True)
    gallery = models.ManyToManyField('GalleryImage', blank=True, related_name="clubs")
    information = models.TextField("Информация о клубе")
    contact_email = models.EmailField("Контактный Email", blank=True, null=True)
    contact_phone = models.CharField("Контактный телефон", max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Клубы"

class GalleryImage(models.Model):
    image = models.ImageField("Изображение", upload_to="club_gallery/")

    def __str__(self):
        return f"Image {self.id}"
    
    class Meta:
        verbose_name_plural = "Фотогалерея"
    
#Новость

class News(models.Model):
    name = models.CharField("Заголовок новости", max_length=255)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name="news")
    photo = models.FileField("Изображение", upload_to="news/", blank=True, null=True)
    description = models.TextField("Описание новости")
    date = models.DateTimeField("Дата новости")

    class Meta:
        verbose_name_plural = "Новости"
    
    def __str__(self):
        return self.name

#Категория книги (Либо жанры)
class Category(models.Model):
    name = models.CharField("Название категории", max_length=255)

    class Meta:
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
       
#Профиль
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField("ФИО", max_length=255, blank=True, null=True)
    photo = models.FileField("Фото", upload_to="profile_photos/", blank=True, null=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    phone_number = models.CharField("Номер телефона", max_length=11, blank=True, null=True)
    reader_ticket = models.CharField("№ читательского билета", max_length=25, blank=True, null=True)
    favorite_categories = models.ManyToManyField(Category, blank=True, related_name="users", verbose_name="Любимые категории")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.favorite_categories.count() > 5:
            raise ValidationError("Вы можете выбрать не более 5 любимых категорий.")

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Профили пользователей"
    
    
#Автор
"""
class Author(models.Model):
    name = models.CharField("ФИО", max_length=255)
    description = models.TextField("Биография")

    class Meta:
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name
"""
    
#Книга

class Book(models.Model):
    FORMAT_CHOICES = [
        ('PRINT', 'Печатное издание'),
        ('DIGITAL', 'Электронный носитель'),
    ]

    title = models.CharField("Название книги", max_length=255)
    author = models.CharField("Авторы", max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    publication_date = models.DateField("Дата публикации", blank=True, null=True)
    publisher = models.CharField("Издатель", max_length=255, blank=True, null=True)
    language = models.CharField("Язык", max_length=50, blank=True, null=True)
    pages = models.IntegerField("Количество страниц", blank=True, null=True)
    cover_image = models.ImageField("Изображение обложки", upload_to="book_covers/", blank=True, null=True)
    description = models.TextField("Описание книги", blank=True)
    file = models.FileField("Файл книги", upload_to="book_files/", blank=True, null=True)
    format = models.CharField("Формат", max_length=10, choices=FORMAT_CHOICES, default='DIGITAL')
    rating = models.DecimalField("Рейтинг", max_digits=3, decimal_places=2, default=0.0, null=True)
    availability = models.BooleanField("Доступность", default=True)
    added_date = models.DateTimeField("Дата добавления", auto_now_add=True)
    views = models.IntegerField("Количество просмотров", default=0, null=True, blank=True)
    downloads = models.IntegerField("Количество загрузок", default=0)
    print_quantity = models.PositiveIntegerField("Количество печатных экземпляров", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title

#Обсуждения, отзывы

class Review(models.Model):
    subject = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField("Отзыв")
    value = models.PositiveIntegerField("Оценка", default=5)
    
    class Meta:
        verbose_name_plural = "Обсуждения"


#Книжная полка - избранное

class Bookshelf(models.Model):
    subject = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField("Приватная полка", default=True)  # Поле для определения приватности

    class Meta:
        verbose_name_plural = "Книжные полки"

    def __str__(self):
        return f"{self.user.username} - {self.subject.title} ({'Приватная' if self.private else 'Публичная'})"

#Обмен

class BookCrossingAd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crossing_ads")
    title = models.CharField("Название книги", max_length=255)
    cover_image = models.ImageField("Фото книги", upload_to="book_crossing_covers/")
    short_description = models.CharField("Краткое описание", max_length=500)
    detailed_description = models.TextField("Подробное описание", blank=True, null=True)
    contact_phone = models.CharField("Номер телефона", max_length=20, blank=True, null=True)
    contact_email = models.EmailField("Email", blank=True)  # Это поле будет заполняться автоматически
    contact_info = models.CharField("Дополнительная контактная информация", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name_plural = "Объявления бук-кроссинга"

    def __str__(self):
        return f"Объявление: {self.title} от {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.contact_email:
            self.contact_email = self.user.email
        super().save(*args, **kwargs)

#Обсуждения

class DiscussionTopic(models.Model):
    title = models.CharField("Название темы", max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    book = models.ForeignKey(Bookshelf, on_delete=models.CASCADE, related_name="discussion_topics", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_topics")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name_plural = "Темы обсуждения"

    def __str__(self):
        return self.title

class DiscussionPost(models.Model):
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussion_posts")
    content = models.TextField("Сообщение")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name_plural = "Сообщения в обсуждениях"

    def __str__(self):
        return f"Сообщение от {self.user.username} в теме {self.topic.title}"
    
#Обратная связь

class Feedback(models.Model):
    CONTACT_METHOD_CHOICES = [
        ('EMAIL', 'Email'),
        ('PHONE', 'Телефон'),
    ]
    
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="feedbacks", null=True, blank=True)
    full_name = models.CharField("ФИО", max_length=255)
    subject = models.CharField("Тема/Вопрос", max_length=255)
    contact_method = models.CharField("Метод связи", max_length=10, choices=CONTACT_METHOD_CHOICES)
    contact_info = models.CharField("Email/Телефон", max_length=255)
    message = models.TextField("Текст обращения")

    def __str__(self):
        return f"Обращение {self.full_name} на тему: {self.subject}"








