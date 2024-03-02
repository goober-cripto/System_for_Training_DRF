from django.contrib import admin

from .models import Product, Lesson, Group


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('creator', 'name', 'start_date', 'cost', 'get_num_accessible_users')
    list_filter = ('creator', 'name', 'start_date', 'cost')
    search_fields = ('creator', 'name', 'start_date', 'cost')

    def get_num_accessible_users(self, obj):
        """
        Возвращает количество клиентов имеющих доступ на данный продукт
        """
        return obj.accessible_users.count()


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'title', 'video_link')
    list_filter = ('product__name', 'video_link')
    search_fields = ('product__name', 'title', 'video_link')

    def product_name(self, obj):
        """
        Возвращает name модели Product
        """
        return obj.product.name if obj.product else ''

    product_name.short_description = 'Product Name'
    product_name.admin_order_field = 'product__name'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'min_users', 'max_users', 'count_users')
    list_filter = ('product', 'name', 'min_users', 'max_users')
    search_fields = ('product', 'name', 'min_users', 'max_users')

    def count_users(self, obj):
        return obj.members.count()
