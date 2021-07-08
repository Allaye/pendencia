
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from todos.serializers import CreateTodoApiViewSerializer
from todos.models import Todo
from todos.serializers import CreateTodoApiViewSerializer
from todos.pagination import CustomPageNumberPagination

class CreateTodoApiView(CreateAPIView):
    '''
        CreateAPIVIEW is a shortcut class from DRF to create resources
    '''
    # serializer class to serialize the request data
    serializer_class  = CreateTodoApiViewSerializer
    permission_classes = (IsAuthenticated,) # protect the endpoint

    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

 
class RetriveTodoApiView(ListAPIView):
    '''
        ListAPIVIEW is a shortcut class from DRF to retrive resources
    '''
    serializer_class = CreateTodoApiViewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

class CreateRetriveApiView(ListCreateAPIView):
    '''
    ListcreateAPIVIEW is a shortcut class from DRF to create and retrive resources
    '''
    serializer_class = CreateTodoApiViewSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'title', 'desc', 'is_complete']
    search_fields = ['id', 'title', 'desc', 'is_complete']
    ordering_fields = ['id', 'title', 'desc', 'is_complete']


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

class RetriveUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CreateTodoApiViewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
