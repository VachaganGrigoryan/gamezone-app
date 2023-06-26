import strawberry

from games import models


@strawberry.django.type(models.Game)
class GameType:
    guid: strawberry.ID
    title: str
    description: str
    image: str
    configs: str

    created_at: str
    updated_at: str

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(is_active=True)


