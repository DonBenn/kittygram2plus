from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.throttling import AnonRateThrottle
from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from rest_framework.throttling import ScopedRateThrottle
from .throttling import WorkingHoursRateThrottle
from rest_framework.pagination import LimitOffsetPagination
from .pagination import CatsPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = None
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name',)
    ordering_fields = ('name', 'birth_year')
    ordering = ('birth_year',)

    #def get_queryset(self):
    #    queryset = Cat.objects.all()
    #    color = self.kwargs['color']
    #    # Через ORM отфильтровать объекты модели Cat
    #    # по значению параметра color, полученного в запросе
    #    queryset = queryset.filter(color=color)
    #    return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer