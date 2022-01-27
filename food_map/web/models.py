from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Restaurant(models.Model):
    """Model, that describes place, where to go"""

    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', max_length=5000)
    location = models.CharField('Местоположение', max_length=75)
    work_time = models.CharField('Время работы', max_length=30)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    type = models.ForeignKey('PlaceType', on_delete=models.PROTECT)
    favourites = models.ManyToManyField(User, related_name='favourites', default=None, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Заведения'

    def get_absolute_url(self):
        return reverse('home-page')


class News(models.Model):
    """Model, that describes News, that are shown"""

    title = models.CharField('Название', max_length=100)
    text = models.TextField('Текст статьи', max_length=9000)
    pub_date = models.DateField('Дата публикации', default=timezone.now, editable=False)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


# class WishListItem(models.Model):
#     """Model, that describes interaction with wishlist"""
#     plan_date = models.DateField('Дата желаемого посещения', blank=True, null=True)
#     comments = models.CharField('Пожелания', blank=True, null=True, max_length=200)
#     place_of_visiting = models.OneToOneField('Restaurant', on_delete=models.PROTECT)
#
#     def __str__(self):
#         return self.place_of_visiting.name
#
#     class Meta:
#         verbose_name = 'Список пожеланий'
#         verbose_name_plural = 'Список пожеланий'


class History(models.Model):
    """Model, that storage all the visited places and experiences about them"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_of_visiting = models.DateField('Дата посещения')
    place_of_visiting = models.ForeignKey('Restaurant', verbose_name='Посещенное заведение', on_delete=models.PROTECT)
    comment = models.CharField('Комментарии', null=True, blank=True, default=None, max_length=2000)

    def __str__(self):
        return f'{self.place_of_visiting.name} - {str(self.date_of_visiting)}'

    class Meta:
        verbose_name = 'Посещенные заведения'
        verbose_name_plural = 'Посещенные заведения'


class PlaceType(models.Model):
    type = models.CharField('Тип зааведения', max_length=40)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип заведения'
        verbose_name_plural = 'Тип заведения'


class Menu(models.Model):
    place = models.ForeignKey('Restaurant', on_delete=models.CASCADE, verbose_name='Заведение',
                              related_name='menu_images')
    menu_image = models.ImageField('Фото меню', null=True, blank=True,
                                   upload_to=f'menu/')

    def __str__(self):
        return self.place.name

    class Meta:
        verbose_name = 'Фото Меню'
        verbose_name_plural = 'Фото Меню'


class Location(models.Model):
    place = models.ForeignKey('Restaurant', on_delete=models.CASCADE, verbose_name='Заведение',
                              related_name='place_location')
    map_location = models.TextField('Расположение', max_length=800)

    def __str__(self):
        return self.place.name

    class Meta:
        verbose_name = 'Расположение мест на карте'
        verbose_name_plural = 'Расположение мест на карте'
