from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from todos.models import Todo
from todos.pagination import CustomPageNumberPagination
from todos.serializers import TodoSerializer


class TodosAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'title', 'desc', 'is_complete']
    search_fields = ['id', 'title', 'desc', 'is_complete']
    ordering_fields = ['id', 'title', 'desc', 'is_complete']

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        username = self.request.user
        qs = Todo.objects.filter(owner=username)
        return qs


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        username = self.request.user
        qs = Todo.objects.filter(owner=username)
        return qs


# Aşağıda ki view lerin yaptığı işleri yukarıda bulunan viewlwe yapıyor örnek olması içi silmedim
class CreateTodoAPIView(CreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ListTodoAPIView(ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Todo.objects.all()

    def get_queryset(self):
        username = self.request.user
        qs = Todo.objects.filter(owner=username)
        return qs
