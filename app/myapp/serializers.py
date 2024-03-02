from rest_framework import serializers, generics
from .models import Product, Lesson

from django.contrib.auth.models import User


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'start_date', 'cost', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()


class ProductStatsSerializer(serializers.ModelSerializer):
    quantity_students = serializers.SerializerMethodField()
    group_fill_percentage = serializers.SerializerMethodField()
    percent_buy_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity_students', 'group_fill_percentage', 'percent_buy_product']

    def get_quantity_students(self, obj):
        """
        Возвращает количество учеников на продукте
        """
        return obj.accessible_users.count()

    def get_group_fill_percentage(self, obj):
        """
        Возвращает процент заполненности групп
        """
        total_groups = obj.group_set.count()
        if total_groups == 0:
            return 0
        total_capacity = sum(group.max_users for group in obj.group_set.all())
        total_members = sum(group.members.count() for group in obj.group_set.all())
        return (total_members / total_capacity) * 100

    def get_percent_buy_product(self, obj):
        """
        Возвращает процент приобретения продукта
        """
        total_users_count = User.objects.count()
        if total_users_count == 0:
            return 0
        access_count = obj.accessible_users.count()
        return (access_count / total_users_count) * 100
