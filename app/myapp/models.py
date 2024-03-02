from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    accessible_users = models.ManyToManyField(User, related_name='accessible_products')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    def has_user_access(self, user):
        """
        Метод для проверки доступа пользователя к продукту (курсу).
        Возвращает True, если пользователь имеет доступ, и False в противном случае.
        """
        return user in self.accessible_users.all()


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_link = models.URLField()

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    min_users = models.PositiveIntegerField()
    max_users = models.PositiveIntegerField()
    members = models.ManyToManyField(User)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
