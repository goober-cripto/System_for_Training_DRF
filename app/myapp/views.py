from rest_framework import generics
from rest_framework import permissions
from django.utils import timezone

from .models import Product, Lesson
from .serializers import ProductSerializer, LessonSerializer, ProductStatsSerializer


class AvailableProductsAPIView(generics.ListAPIView):
    """
    Возвращает список продуктов, доступных для покупки, включая основную информацию о продукте и количество уроков,
    принадлежащих продукту.
    """
    queryset = Product.objects.filter(start_date__gt=timezone.now())  # Получаем доступные продукты
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class LessonsByProductAPIView(generics.ListAPIView):
    """
    Возвращает список уроков по конкретному продукту, к которому пользователь имеет доступ.
    """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Получает список уроков по конкретному продукту, к которому пользователь имеет доступ.
        """
        user = self.request.user
        product_id = self.kwargs['product_id']
        return Lesson.objects.filter(product_id=product_id, product__accessible_users=user)


class ProductStatsAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductStatsSerializer