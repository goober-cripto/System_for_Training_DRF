from django.urls import path, include
from .views import AvailableProductsAPIView, LessonsByProductAPIView

app_name = 'myapp'

urlpatterns = [
    path('api/v1/', include([
        path('available-products/', AvailableProductsAPIView.as_view(), name='available-products'),
        path('lessons-by-product/<int:product_id>/', LessonsByProductAPIView.as_view(), name='lessons-by-product'),
    ])),
]
