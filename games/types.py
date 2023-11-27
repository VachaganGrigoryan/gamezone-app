from typing import List, Optional

import strawberry
from asgiref.sync import sync_to_async
from jwtberry.permission import IsAuthenticated
from strawberry import auto

from core.json import JSON
from core.utils import url_resolver
from games import models as m


@strawberry.django.type(m.Game)
class GameType:
    guid: strawberry.ID
    title: auto
    description: auto

    configs: Optional[JSON]

    created_at: auto
    updated_at: auto

    @strawberry.field
    def image(self, info) -> Optional[str]:
        return url_resolver(info, self.image)

    @classmethod
    def all(cls, info):
        return cls.get_queryset(m.Game.objects.all(), info)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(is_active=True)


@strawberry.type
class ZoneQuery:

    @strawberry.django.field(permission_classes=[IsAuthenticated])
    def games(self, info) -> List[GameType]:
        return GameType.all(info)
