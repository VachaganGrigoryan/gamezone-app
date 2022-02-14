import django_filters

from account.models import User


class UserFilter(django_filters.FilterSet):

    order_by = django_filters.OrderingFilter(
        fields=(
            ('first_name', 'last_name'),
        )
    )

    class Meta:
        model = User
        fields = (
            'guid',
            'first_name',
            'last_name',
        )
