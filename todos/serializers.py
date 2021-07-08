from django.db.models import fields
from rest_framework import serializers
from todos.models import Todo

class CreateTodoApiViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todo
        fields = ('id','title', 'desc', 'is_complete')

