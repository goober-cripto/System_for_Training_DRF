from django.db.models import Count, signals
from django.dispatch import receiver
from django.utils import timezone

from .models import Group, Product
import logging


@receiver(signals.m2m_changed, sender=Product.accessible_users.through)
def distribute_users_to_groups(sender, instance, action, **kwargs) -> None:
    """
    Распределяет пользователей по группам при изменении доступа к продукту.
    """
    if action == 'post_add':
        logging.info("Signal handler was triggered for granting access to product.")

        product = instance
        users = product.accessible_users.all()
        total_users_count = users.count()
        groups = Group.objects.filter(product=product)

        if total_users_count == 0 or groups.count() == 0:
            return

        # Проверяем, начался ли продукт
        if product.start_date > timezone.now():
            # Если продукт ещё не начался, пересобираем группы
            distribute_users_evenly(groups, users)
        else:
            # Иначе распределяем пользователей по группам до максимального значения
            distribute_users_to_max_capacity(groups, users)


def distribute_users_evenly(groups, users) -> None:
    """
    Распределяет пользователей по группам так, чтобы количество участников было примерно одинаковым.
    """
    # Сортируем группы по количеству участников в них
    sorted_groups = groups.annotate(num_members=Count('members')).order_by('num_members')
    # Распределяем пользователей по группам так, чтобы количество участников было примерно одинаковым
    group_index = 0
    for user in users:
        group = sorted_groups[group_index]
        group.members.add(user)
        group_index = (group_index + 1) % len(sorted_groups)


def distribute_users_to_max_capacity(groups, users) -> None:
    """
    Распределяет пользователей по группам до максимального значения.
    """
    # Сортируем группы по текущему количеству участников
    sorted_groups = groups.annotate(num_members=Count('members')).order_by('num_members')

    # Распределяем пользователей по группам до максимального значения
    for group in sorted_groups:
        max_members = group.max_users
        num_members = group.members.count()
        if num_members < max_members:
            members_to_add = min(max_members - num_members, len(users))
            group.members.add(*users[:members_to_add])
            users = users[members_to_add:]
            if not users:
                break
